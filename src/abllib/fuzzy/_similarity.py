"""Module containing the similarity function"""

import numpy

from ..alg import levenshtein_distance

def similarity(target: str, candidate: str, threshold: int) -> float:
    """
    Checks how closely two strings match.
    
    Returns a float value between 0.0 and 1.0 (inclusive).
    """

    edit_dist = levenshtein_distance(target, candidate)
    if edit_dist <= threshold:
        return numpy.round(1.0 / (edit_dist + 1), 2)

    score = 0.0
    candidates_len = len(candidate.split(" "))
    for inner_target in target.split(" "):
        min_edit_dist = 1000

        for inner_candidate in candidate.split(" "):
            edit_dist = levenshtein_distance(inner_target, inner_candidate)

            if edit_dist <= min(len(inner_target) // 3, len(inner_candidate) // 3, threshold):
                min_edit_dist = min(edit_dist, min_edit_dist)

        if min_edit_dist < 1000:
            score += _calc_score(min_edit_dist) / candidates_len

    if score > 0.0:
        return numpy.round(score, 2)

    return 0.0

def _calc_score(edit_dist: int) -> float:
    return 1 / (0.05 * (edit_dist ** 2) + 1)
