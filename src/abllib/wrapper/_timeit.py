"""Module containing the timeit wrapper"""

import functools
from time import perf_counter_ns
from typing import Any, Callable

from abllib import convert
from abllib.log import LogLevel
from abllib.wrapper._base_log_wrapper import BaseLogWrapper

class timeit(BaseLogWrapper):
    """
    Decorate a function, which logs the execution time of this function.
    The values are logged with log level DEBUG, so make sure you configured your logger properly.

    If the optional argument logger is set and of type logging.Logger, log the time to that logger.

    If the optional argument logger is set and of type str, request that logger and log the time.

    Otherwise, the time is logged to the root logger.

    Can also be directly used as a wrapper.
    """

    def __call__(self, func: Callable) -> Callable:
        """Called when the class instance is used as a decorator"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """The wrapped function that is called on function execution"""

            start = perf_counter_ns()

            res = func(*args, **kwargs)

            elapsed = float(perf_counter_ns() - start)
            elapsed *= (10 ** -9)
            log_msg = f"{func.__name__}: {convert.as_time(elapsed)} elapsed"
            self.log(log_msg, LogLevel.DEBUG)
            return res

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper
