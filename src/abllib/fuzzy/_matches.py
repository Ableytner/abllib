"""Module containing the matches function"""

from ..alg import levenshtein_distance

# pylint: disable-next=too-many-return-statements
def matches(target: str, candidate: str, threshold: int) -> float:
    """
    Checks how closely two strings match.
    
    Returns a float value between 0.0 and 1.0 (inclusive)
    """

    if target in candidate:
        return 1.0

    # threshold of 0 means that the target needs to be equal or contained as-is
    if threshold == 0:
        return 0.0

    score = 0.0
    targets_len = len(target.split(" "))
    candidates_len = len(candidate.split(" "))
    for inner_target in target.split(" "):
        for inner_candidate in candidate.split(" "):
            if matches(inner_target, inner_candidate, 0) > 0.0:
                score += (1.0 / targets_len) * (1.0 / candidates_len)
    if score > 0.0:
        return score

    # threshold of 1 means that subwords can also match
    if threshold == 1:
        return 0.0

    edit_dist = levenshtein_distance(target, candidate)
    if edit_dist <= threshold:
        return 1.0 / edit_dist

    # threshold of 2 means that the target or a subword needs to be mostly equal
    if threshold == 2:
        return 0.0

    score = 0.0
    targets_len = len(target.split(" "))
    candidates_len = len(candidate.split(" "))
    for inner_target in target.split(" "):
        for inner_candidate in candidate.split(" "):
            edit_dist = levenshtein_distance(inner_target, inner_candidate)
            if edit_dist <= min(len(inner_target) // 3, len(inner_candidate) // 3, threshold):
                score += (1.0 / targets_len) * (1.0 / candidates_len) * (1.0 / edit_dist)
    if score > 0.0:
        return score

    # threshold of 3 means that subwords must be pretty equal
    if threshold == 3:
        return 0.0

    return 0.0
