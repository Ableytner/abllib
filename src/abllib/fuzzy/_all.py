"""A module containing the fuzzy search function"""

from ._matchresult import MatchResult
from ._similarity import similarity
from .. import log

logger = log.get_logger("test")

def match_all(target: str, candidates: list[str | tuple[str]], threshold: int = 5) -> list[MatchResult]:
    """
    Search for all candidates matching the target. Applies fuzzy logic when comparing.

    In order to successfully find a candidate, at least one of two conditions need to be true:
    * the edit distance (levenshtein distance) needs to be smaller than >threshold<
    * a single word (>target< split at ' ') needs to have an edit distance smaller than (len(>word<) / 3) + 1

    Returns a list of ints which represent the indexes in candidates that matched the search.
    """

    # TODO: type checking with abllib.type module

    if threshold < 0:
        raise ValueError("Threshold needs to be >= 0")

    results = []
    for i, candidate in enumerate(candidates):
        curr_result = _match_single_candidate(target, candidate, threshold)
        if curr_result is not None:
            results.append(MatchResult(curr_result.score, curr_result.value, i, curr_result.inner_index))

    return results

def _match_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> MatchResult | None:
    if isinstance(candidate, str):
        score = similarity(target, candidate, threshold)
        return MatchResult(score, candidate) if score > 0.0 else None

    result = MatchResult(0.0)
    for i, inner_candidate in enumerate(candidate):
        score = similarity(target, inner_candidate, threshold)
        if score > result.score:
            result = MatchResult(score, candidate, inner_index=i)

    return result if result.score > 0.0 else None
