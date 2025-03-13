"""A module containing fuzzy search / fuzzy matching-related functionality"""

from .match import match
from .search import search

__exports__ = [
    match,
    search
]
