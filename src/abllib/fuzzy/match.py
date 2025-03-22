"""A module containing the fuzzy match function"""

from ._similarity import similarity

def match(target: str | tuple[str], candidates: list[str | tuple[str]], threshold: int = 5) \
    -> tuple[int | None, float]:
    """
    Match the target to the most similar candidate. Applies fuzzy logic when comparing.

    In order to successfully match a candidate, at least one of two conditions need to be true:
    * the edit distance (levenshtein distance) needs to be smaller than >threshold<
    * a single word (>target< split at ' ') needs to have an edit distance smaller than len(>word<) / 3

    After that, it chooses the closest-matching candidate

    Returns a tuple[int, float], which represents the index in candidates that matched the closest,
    and the similarity score, which is between 0.0 and 1.0
    """

    # TODO: type checking with abllib.type module

    if threshold < 0:
        raise ValueError("Threshold needs to be >= 0")

    closest_match = (None, 0.0)
    for i, candidate in enumerate(candidates):
        curr_similarity = _matches_single_candidate(target, candidate, threshold)
        if curr_similarity > closest_match[1]:
            closest_match = (i, curr_similarity)

    return closest_match

def _matches_single_candidate(target: str | tuple[str], candidate: str | tuple[str], threshold: int) -> float:
    if isinstance(candidate, str):
        return similarity(target, candidate, threshold)

    max_similarity = 0.0
    for inner_candidate in candidate:
        current_similarity = similarity(target, inner_candidate, threshold)
        max_similarity = max(current_similarity, max_similarity)

    return max_similarity
