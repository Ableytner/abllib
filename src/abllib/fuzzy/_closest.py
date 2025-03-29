"""A module containing the fuzzy match function"""

from ._matchresult import MatchResult
from ._similarity import similarity

def match_closest(target: str, candidates: list[str | tuple[str]], threshold: int = 5) -> MatchResult:
    """
    Match the target to the most similar candidate. Applies fuzzy logic when comparing.

    In order to successfully match a candidate, at least one of two conditions need to be true:
    * the edit distance (levenshtein distance) needs to be smaller than >threshold<
    * a single word (>target< split at ' ') needs to have an edit distance smaller than (len(>word<) / 3) + 1

    After that, it chooses the closest-matching candidate

    Returns a tuple[int, float], which represents the index in candidates that matched the closest,
    and the similarity score, which is between 0.0 and 1.0
    """

    # TODO: type checking with abllib.type module

    if threshold < 0:
        raise ValueError("Threshold needs to be >= 0")

    result = MatchResult(0.0)
    for i, candidate in enumerate(candidates):
        curr_result = _matches_single_candidate(target, candidate, threshold)
        if curr_result.score > result.score:
            result = MatchResult(curr_result.score, curr_result.value, i, curr_result.inner_index)

    return result

def _matches_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> MatchResult:
    if isinstance(candidate, str):
        score = similarity(target, candidate, threshold)
        return MatchResult(score, candidate)

    max_result = MatchResult(0.0)
    for inner_candidate in candidate:
        score = similarity(target, inner_candidate, threshold)
        if score > max_result.score:
            max_result = MatchResult(score, candidate)

    return max_result
