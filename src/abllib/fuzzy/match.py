"""A module containing the fuzzy match function"""

import numpy

from ._similarity import similarity

def match(target: str | tuple[str], candidates: list[str] | list[tuple[str]], threshold: int = 5) \
    -> tuple[int | None, float]:
    """
    Match the target to the most similar candidate. Applies fuzzy logic when comparing.

    The behaviour for different thresholds is as follows:
    * 0: the candidate has to contain the exact target
    * 1: subwords in candidate or target need to match exactly
    * 2: the candidate adn target need to have an edit distance of at most >threshold<
    * 3: the subwords need to have an edit distance of at most min( >threshold< or len(>subword<) // 3 )
    * 4+: unchanged behaviour

    Returns a tuple[int, float], which represents the index in candidates that matched the closest,
    and the similarity, which is between 0.0 and 1.0
    """

    # TODO: type checking with abllib.type module

    # if there are no candidates, the search fails
    if len(candidates) == 0:
        raise ValueError("Expected at least one candidate")

    if threshold < 0:
        raise ValueError("Threshold needs to be >= 0")

    closest_match = (None, 0.0)
    for i, candidate in enumerate(candidates):
        curr_similarity = _matches_single_candidate(target, candidate, threshold)
        if curr_similarity > closest_match[1]:
            closest_match = (i, numpy.round(curr_similarity, 2))

    return closest_match

def _matches_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> float:
    if isinstance(candidate, str):
        return similarity(target, candidate, threshold)

    max_similarity = 0.0
    for inner_candidate in candidate:
        current_similarity = similarity(target, inner_candidate, threshold)
        max_similarity = max(current_similarity, max_similarity)

    return max_similarity
