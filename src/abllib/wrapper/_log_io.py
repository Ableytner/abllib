"""Module containing the log_io wrapper"""

import functools
from logging import Logger
from typing import Callable, Any

from .. import log

class log_io():
    """
    Decorate a function, which logs any passed arguments and return values.
    The values are logged with log level DEBUG, so make soure you configured your logger properly.

    If the optional argument logger is set and of type logging.Logger, log the values to that logger.

    If the optional argument logger is set and of type str, request that logger and log the values.

    Otherwise, the values are logged to the root logger.
    """

    def __new__(cls, logger: str | Logger | None | Callable = None):
        inst = super().__new__(cls)

        # used directly as a wrapper
        if callable(logger):
            inst.logger = log.get_logger()
            return inst(logger)

        # logger is the loggers' name
        if isinstance(logger, str):
            _logger = log.get_logger(logger)
        # logger is a logging.Logger object
        elif isinstance(logger, Logger):
            _logger = logger

        inst.logger = _logger
        return inst

    logger: Logger

    def __call__(self, func: Callable):
        """Called when the class instance is used as a decorator"""

        def wrapper(*args, **kwargs):
            """The wrapped function that is called on function execution"""

            res = func(*args, **kwargs)

            self.logger.debug(f"func: {func.__name__}")
            arg_str = ", ".join([self._format(item) for item in args] + [f"{key}={self._format(value)}" for key, value in kwargs.items()])
            self.logger.debug(f"in  : {arg_str}")
            self.logger.debug(f"out : {self._format(res)}")

            return res

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper

    def _format(self, arg: Any) -> str:
        if isinstance(arg, str):
            return f"\"{arg}\""
        
        return str(arg)
