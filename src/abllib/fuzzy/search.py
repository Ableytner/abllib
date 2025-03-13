"""A module containing the fuzzy search functionality"""

from ._matches import matches

def search(target: str | tuple[str], candidates: list[str] | list[tuple[str]], threshold: int = 5) -> list[int]:
    """
    Search for candidates matching the target. Applies fuzzy logic when comparing.

    The behaviour for different thresholds is as follows:
    * 0: the candidate has to contain the exact target
    * 1: subwords in candidate or target need to match exactly
    * 2: the candidate adn target need to have an edit distance of at most >threshold<
    * 3: the subwords need to have an edit distance of at most min( >threshold< or len(>subword<) // 3 )
    * 4+: unchanged behaviour

    Returns a list of ints which represent the indexes in candidates that matched the search.
    """

    # TODO: type checking with abllib.type module

    # if there are no candidates, the search fails
    if len(candidates) == 0:
        return []

    if threshold < 0:
        raise ValueError("Threshold needs to be >= 0")

    matched_candidates = []
    for i, candidate in enumerate(candidates):
        if _matches_single_candidate(target, candidate, threshold):
            matched_candidates.append(i)

    return matched_candidates

def _matches_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> bool:
    if isinstance(candidate, str):
        return matches(target, candidate, threshold)

    for inner_candidate in candidate:
        if matches(target, inner_candidate, threshold):
            return True

    return False
