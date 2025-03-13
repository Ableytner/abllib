"""Module containing the similarity function"""

from ..alg import levenshtein_distance

# pylint: disable-next=too-many-return-statements
def similarity(target: str, candidate: str, threshold: int) -> float:
    """
    Checks how closely two strings match.
    
    Returns a float value between 0.0 and 1.0 (inclusive).
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
        max_similarity = 0.0

        for inner_candidate in candidate.split(" "):
            curr_similarity = similarity(inner_target, inner_candidate, 0)
            max_similarity = max(curr_similarity, max_similarity)

        if max_similarity > 0.0:
            score += _calc_score(targets_len, candidates_len, max_similarity)

    if score > 0.0:
        return score

    # threshold of 1 means that subwords can also match
    if threshold == 1:
        return 0.0

    edit_dist = levenshtein_distance(target, candidate)
    if edit_dist <= threshold:
        return 1.0 / (edit_dist + 1)

    # threshold of 2 means that the target or a subword needs to be mostly equal
    if threshold == 2:
        return 0.0

    score = 0.0
    targets_len = len(target.split(" "))
    candidates_len = len(candidate.split(" "))
    for inner_target in target.split(" "):
        max_similarity = 0.0

        for inner_candidate in candidate.split(" "):
            edit_dist = levenshtein_distance(inner_target, inner_candidate)
            curr_similarity = 1 / (edit_dist + 1)

            if edit_dist <= min(len(inner_target) // 3, len(inner_candidate) // 3, threshold) \
               and curr_similarity > max_similarity:
                max_similarity = curr_similarity

        if max_similarity > 0.0:
            score += _calc_score(targets_len, candidates_len, max_similarity)

    if score > 0.0:
        return score

    # threshold of 3 means that subwords must be pretty equal
    if threshold == 3:
        return 0.0

    return 0.0

def _calc_score(targets_len: int, candidates_len: int, sim: float) -> float:
    assert targets_len > 0
    assert candidates_len > 0
    assert sim >= 0.0
    assert sim <= 1.0

    # always divides the smaller count throught the larger count
    # this always results in a number <= 1.0
#    base_score = min(targets_len, candidates_len) / max(targets_len, candidates_len)
#    score += base_score * similarity

    return (1 / candidates_len) * sim
