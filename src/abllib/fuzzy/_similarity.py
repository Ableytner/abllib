"""Module containing the similarity function"""

import math

import numpy as np

from abllib import error
from ..alg import levenshtein_distance

def similarity(target: str, candidate: str, threshold: int) -> float:
    """
    Checks how closely two strings match. (Version 2)
    
    Returns a float value between 0.0 and 1.0 (inclusive), where 1.0 is a perfect match.
    """

    score = max(
        _similarity_simple(target, candidate, threshold),
        _similarity_with_inner(target, candidate, threshold)
    )
    score = np.round(score, 2)

    if score < 0.0 or score > 1.0:
        raise error.InternalCalculationError(f"Score {score} is not in acceptable range 0.0 <= score <= 1.0")

    return score

def _similarity_simple(target: str, candidate: str, threshold: int) -> float:
    edit_dist = levenshtein_distance(target, candidate)

    if edit_dist > threshold:
        return 0.0

    similar_chars = len(candidate) - edit_dist
    return similar_chars / len(candidate)

def _similarity_with_inner(target: str, candidate: str, threshold: int) -> float:
    scores_array = _construct_scores_array(target, candidate, threshold)

    original_size = scores_array.shape[1]

    if scores_array.shape[0] != scores_array.shape[1]:
        scores_array = _strip_scores_array(scores_array)

    if scores_array.shape[0] > 8:
        raise error.InternalCalculationError(f"Calculating {math.factorial(scores_array.shape[0])} "
                                             + "combinations is too expensive")

    score = _alg(scores_array, 0.0, original_size)

    return score

def _construct_scores_array(target: str, candidate: str, threshold: int) -> np.ndarray:
    targets = target.split(" ")
    candidates = candidate.split(" ")

    scores_array = np.full((len(targets), len(candidates)), fill_value=0.0)

    # construct scores_matrix 2d array
    for i_target, inner_target in enumerate(targets):
        for i_candidate, inner_candidate in enumerate(candidates):
            edit_dist = levenshtein_distance(inner_target, inner_candidate)

            max_dist_by_target = (len(inner_target) // 3) + 1
            max_dist_by_candidate = (len(inner_candidate) // 3) + 1
            max_allowed_dist = min(max_dist_by_target, max_dist_by_candidate, threshold)

            # check if edit distance is within bounds
            if edit_dist <= max_allowed_dist:
                similar_chars = len(inner_candidate) - edit_dist
                score = similar_chars / len(inner_candidate)
                scores_array[i_target][i_candidate] = score

    return scores_array

def _strip_scores_array(scores_array: np.ndarray) -> np.ndarray:
    # fewer rows than columns
    while scores_array.shape[0] < scores_array.shape[1]:
        # we want to sum up all columns
        # and find the smallest sum
        # and delete that column
        i_row = 0
        while i_row < scores_array.shape[1]:
            sums = scores_array.sum(0)
            i_min = np.argmin(sums)
            scores_array = np.delete(scores_array, i_min, 1)

            i_row += 1

    # fewer columns than rows
    while scores_array.shape[1] < scores_array.shape[0]:
        # we want to sum up all rows
        # and find the smallest sum
        # and delete that row
        i_column = 0
        while i_column < scores_array.shape[0]:
            sums = scores_array.sum(1)
            i_min = np.argmin(sums)
            scores_array = np.delete(scores_array, i_min, 0)

            i_column += 1

    return scores_array

def _alg(data: np.ndarray, combined_score: float, orig_size: int) -> float:
    """
    I have no idea what to call this algorithm.
    
    It generates all unique combinations of a 2d input array such that in each combination,
    each row and each column only occurs once.

    This process is done recursively and is quite inefficient,
    as the number of combinations equals !n, where n is the number of rows / columns.
    """

    if data.shape[0] == 1:
        combined_score += data[0][0]
        return combined_score / orig_size

    row_index = 0
    col_index = 0
    max_score = 0.0
    scores = []

    while row_index < data.shape[0]:
        reduced_data = _reduce(data, row_index, col_index)

        score = _alg(reduced_data, combined_score + data[row_index][col_index], orig_size)
        scores.append(score)
        max_score = max(score, max_score)

        row_index += 1

    return max_score

def _reduce(data: np.ndarray, r_index: int, c_index: int) -> np.ndarray:
    # delete a row
    data = np.delete(data, r_index, 0)
    # delete a column
    return np.delete(data, c_index, 1)
