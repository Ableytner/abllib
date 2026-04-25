"""Module containing the log_io wrapper"""

from __future__ import annotations

import functools
from logging import Logger
from typing import Any, Callable

from abllib import log
from abllib.error import WrongTypeError

class BaseLogWrapper():
    """
    Base class for all decorators that log something.

    If the optional argument logger is set and of type logging.Logger, use that logger.

    If the optional argument logger is set and of type str, request and use that loggers.

    Otherwise, use the root logger.

    Can also be directly used as a wrapper.
    """

    def __new__(cls, # type: ignore[misc]
                logger: str | Logger | Callable | None = None,
                handler: Callable[[str], None] | None = None) -> BaseLogWrapper | Callable:
        inst = super().__new__(cls)

        # used directly as a wrapper
        if callable(logger):
            inst.logger = log.get_logger()
            inst.handler = None
            wrapped_func = inst(logger)
            # https://stackoverflow.com/a/17705456/15436169
            functools.update_wrapper(wrapped_func, logger)
            return wrapped_func

        # logger is the loggers' name
        if isinstance(logger, str):
            _logger = log.get_logger(logger)
        # logger is a logging.Logger object
        elif isinstance(logger, Logger):
            _logger = logger
        elif logger is None:
            _logger = log.get_logger()
        else:
            raise WrongTypeError.with_values(logger, (str, Logger, None))

        inst.logger = _logger
        inst.handler = handler
        return inst

    logger: Logger
    handler: Callable[[str], None] | None

    def log(self, message: str, log_level: log.LogLevel | int) -> None:
        """
        Log the given message.

        If self.handler is not None, ignore log_level and use handler.

        Else use self.logger with given log_level.
        """

        if self.handler is not None:
            self.handler(message)
            return

        if isinstance(log_level, log.LogLevel):
            log_level = log_level.value
        self.logger.log(log_level, message)

    def log_exception(self, exc: Exception) -> None:
        """
        Log the given exception.

        If self.handler is not None, ignore log_level and use handler.

        Else use self.logger with given log_level.
        """

        if self.handler is not None:
            self.handler(f"{exc.__class__.__name__}: {exc}")
            return

        self.logger.exception(exc)

    def __call__(self, func: Callable) -> Callable:
        """Called when the class instance is used as a decorator"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """The wrapped function that is called on function execution"""

            raise NotImplementedError()

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper
