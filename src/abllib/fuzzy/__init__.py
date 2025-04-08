"""A module containing fuzzy matching-related functionality"""

from ._all import match_all
from ._closest import match_closest
from ._matchresult import MatchResult
from ._similarity import Similarity

def similarity(target: str, candidate: str) -> float:
    """A helper function for using abllib.fuzzy.similarity"""

    return Similarity(target, candidate).calculate()

__exports__ = [
    match_all,
    match_closest,
    MatchResult,
    Similarity,
    similarity
]
