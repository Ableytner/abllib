"""Module containing the deprecated wrapper"""

from __future__ import annotations

import functools
import traceback
from typing import Any, Callable

from abllib import log
from abllib.error import DeprecatedError

logger = log.get_logger("deprecated")

class deprecated():
    """
    Mark a function or class as deprecated.

    Calling the function logs a deprecation warning.

    If the optional arg raise_exec is set, raises a deprecation error instead.
    """

    def __new__(cls, # type: ignore[misc]
                message: str | None | Callable = None,
                raise_exec: bool = False) -> _Deprecated | Callable:
        if not raise_exec:
            return deprecated.warning(message)

        return deprecated.error(message)

    @staticmethod
    def warning(message: str | None | Callable = None) -> _Deprecated | Callable:
        """
        Mark a function or class as deprecated.

        Calling the function logs a deprecation warning.
        """

        # deprecated.warning was called with a custom message
        if not callable(message):
            return _Deprecated(message, False)

        # deprecated.warning was not called, only used as a decorator
        return _Deprecated(None, False)(message)

    @staticmethod
    def error(message: str | None | Callable = None) -> _Deprecated | Callable:
        """
        Mark a function or class as deprecated.

        Calling the function raises a DeprecatedError.
        """

        # deprecated.error was called with a custom message
        if not callable(message):
            return _Deprecated(message, True)

        # deprecated.error was not called, only used as a decorator
        return _Deprecated(None, True)(message)

class _Deprecated():
    def __init__(self, message: str | None, raise_exec: bool) -> None:
        self._message = message
        self._raise_exec = raise_exec

    _message: str | None
    _raise_exec: bool

    def __call__(self, func: Callable) -> Callable:
        """Called when the class instance is used as a decorator"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """The wrapped function that is called on function execution"""

            # the default message is used
            if self._message is None:
                traces = traceback.format_list(traceback.extract_stack())
                traces.reverse()
                usage_line = traces[1].split("\n")[0].strip()
                message = f"The functionality '{func.__name__}' is deprecated but used here: {usage_line}"
            # the message was overwritten
            else:
                message = str(self._message)

            if self._raise_exec:
                raise DeprecatedError(message)

            logger.warning(message)

            return func(*args, **kwargs)

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper
