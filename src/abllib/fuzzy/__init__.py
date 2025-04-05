"""A module containing fuzzy matching-related functionality"""

from ._all import match_all
from ._closest import match_closest
from ._matchresult import MatchResult

__exports__ = [
    match_all,
    match_closest,
    MatchResult
]
