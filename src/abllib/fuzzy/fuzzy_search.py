"""A module containing the fuzzy search functionality"""

from ..alg import levenshtein_distance

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

    matches = []
    for i, candidate in enumerate(candidates):
        if _matches_single_candidate(target, candidate, threshold):
            matches.append(i)

    return matches

def _matches_single_candidate(target: str, candidate: str | tuple[str], threshold: int) -> bool:
    if isinstance(candidate, str):
        return _matches(target, candidate, threshold)

    for inner_candidate in candidate:
        if _matches(target, inner_candidate, threshold):
            return True

    return False

# pylint: disable-next=too-many-return-statements
def _matches(target: str, candidate: str, threshold: int) -> bool:
    if target in candidate:
        return True

    # a threshold of 0 means that the target needs to be equal or contained as-is
    if threshold == 0:
        return False

    for inner_target in target.split(" "):
        for inner_candidate in candidate.split(" "):
            if _matches(inner_target, inner_candidate, 0):
                return True

    # a threshold of 1 means that subwords can also match
    if threshold == 1:
        return False

    if levenshtein_distance(target, candidate) <= threshold:
        return True

    # a threshold of 2 means that the target or a subword needs to be mostly equal
    if threshold == 2:
        return False

    for inner_target in target.split(" "):
        for inner_candidate in candidate.split(" "):
            if levenshtein_distance(inner_target, inner_candidate) <= \
               min(len(inner_target) // 3, len(inner_candidate) // 3, threshold):
                return True

    # a threshold of 3 means that subwords must be pretty equal
    if threshold == 3:
        return False

    return False
