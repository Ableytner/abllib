"""Module containing the log_error wrapper"""

from __future__ import annotations

import functools
from typing import Any, Callable

from abllib.wrapper._base_log_wrapper import BaseLogWrapper

class log_error(BaseLogWrapper):
    """
    Decorate a function, which logs any exception occurring during execution.

    If the optional argument logger is set and of type logging.Logger, log the error to that logger.

    If the optional argument logger is set and of type str, request that logger and log the error.

    If the optional argument handler is set, forwards the error message to that function.

    Otherwise, the error is logged to the root logger.

    Can also be directly used as a wrapper.
    """

    def __call__(self, func: Callable) -> Callable:
        """Called when the class instance is used as a decorator"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """The wrapped function that is called on function execution"""

            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_exception(e)
                raise

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper
