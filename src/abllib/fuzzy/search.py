"""A module containing the fuzzy search function"""

from ._similarity import similarity
from .. import log

logger = log.get_logger("test")

def search(target: str | tuple[str], candidates: list[str] | list[tuple[str]], threshold: int = 5) -> list[int]:
    """
    Search for candidates matching the target. Applies fuzzy logic when comparing.

    In order to successfully find a candidate, at least one of two conditions need to be true:
    * the edit distance (levenshtein distance) needs to be smaller than >threshold<
    * a single word (>target< split at ' ') needs to have an edit distance smaller than len(>word<) / 3

    Returns a list of ints which represent the indexes in candidates that matched the search.
    """

    # TODO: type checking with abllib.type module

    if threshold < 0:
        raise ValueError("Threshold needs to be >= 0")

    matched_candidates = []
    for i, candidate in enumerate(candidates):
        if _matches_single_candidate(target, candidate, threshold):
            matched_candidates.append(i)

    return matched_candidates

def _matches_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> bool:
    score = _calculate_single_candidate(target, candidate, threshold)
    return score > 0.0

def _calculate_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> bool:
    if isinstance(candidate, str):
        return similarity(target, candidate, threshold)

    max_score = 0.0
    for inner_candidate in candidate:
        score = similarity(target, inner_candidate, threshold)
        max_score = max(score, max_score)

    return max_score
