"""Module containing the singleuse wrapper function"""

import functools

from ..error import CalledMultipleTimesError

def singleuse(func):
    """The decorator, which is called at program start"""

    was_called = [False]

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """The wrapped function that is called on function execution"""

        if was_called[0]:
            raise CalledMultipleTimesError()

        was_called[0] = True

        return func(*args, **kwargs)

    return wrapper
