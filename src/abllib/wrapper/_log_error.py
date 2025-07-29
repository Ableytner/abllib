"""Module containing the log_error wrapper"""

import functools
from logging import Logger
from typing import Callable

from .. import log
from ..error import ArgumentCombinationError

class log_error():
    """
    Decorate a function, which logs any exception occuring during execution.

    If the optional argument logger is set and of type logging.Logger, log the error to that logger.

    If the optional argument logger is set and of type str, request that logger and log the error.

    If the optional argument handler is set, forwards the error message to that function.

    Otherwise, the error is logged to the root logger.
    """

    def __new__(cls, logger: str | Logger | None | Callable = None, handler: Callable | None = None):
        if logger is None and handler is None:
            raise ArgumentCombinationError("Either logger or handler need to be provided")

        # used directly as a wrapper
        if callable(logger):
            _handler = log.get_logger().exception
            inst = super().__new__(cls)
            inst.handler = _handler
            return inst(logger)

        # logger is the loggers' name
        if isinstance(logger, str):
            _handler = log.get_logger(logger).exception
        # logger is a logging.Logger object
        elif isinstance(logger, Logger):
            _handler = logger.exception
        # handler is given
        else:
            # pylint: disable-next=unnecessary-lambda-assignment
            _handler = lambda exc: handler(f"{exc.__class__.__name__}: {exc}")

        inst = super().__new__(cls)
        inst.handler = _handler
        return inst

    handler: Callable

    def __call__(self, func: Callable):
        """Called when the class instance is used as a decorator"""

        def wrapper(*args, **kwargs):
            """The wrapped function that is called on function execution"""

            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.handler(e)
                raise

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper
