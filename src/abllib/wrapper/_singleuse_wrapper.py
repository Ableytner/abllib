"""Module containing the singleuse wrapper function"""

import functools
from typing import Any, Callable

from abllib.error import CalledMultipleTimesError

def singleuse(func: Callable) -> Callable:
    """
    Make a function single-use only.
    If the function raised an exception, it is not seen as called and can be used again.

    Calling the function twice raises an error.CalledMultipleTimesError.
    """

    was_called = [False]

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """The wrapped function that is called on function execution"""

        if was_called[0]:
            raise CalledMultipleTimesError()

        res = func(*args, **kwargs)

        was_called[0] = True

        return res

    # https://stackoverflow.com/a/17705456/15436169
    functools.update_wrapper(wrapper, func)

    return wrapper
