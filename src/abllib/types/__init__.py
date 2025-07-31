"""A module containing typing-related functionality"""

from typing import Any, Callable

from ._enforce import enforce, enforce_var, enforce_args

__exports__ = [
    Any,
    Callable,
    enforce,
    enforce_var,
    enforce_args
]
