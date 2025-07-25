"""A module containing the logger creation"""

import atexit
import logging
import sys
from enum import Enum
from typing import Literal

from . import error, fs
from ._storage import InternalStorage

DEFAULT_LOG_LEVEL = logging.INFO

class LogLevel(Enum):
    """An enum holding log levels"""

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    ALL = 1
    NOTSET = logging.NOTSET

    def __eq__(self, other):
        return self is other or self.value == other

    def __ne__(self, other):
        return self is not other and self.value != other

    # for more details look here:
    # https://stackoverflow.com/a/72664895/15436169
    def __hash__(self):
        return hash(self.value)

def initialize(log_level: Literal[LogLevel.CRITICAL]
                          | Literal[LogLevel.ERROR]
                          | Literal[LogLevel.WARNING]
                          | Literal[LogLevel.INFO]
                          | Literal[LogLevel.DEBUG]
                          | Literal[LogLevel.ALL]
                          | int
                          | None = None):
    """
    Initialize the custom logging module.

    This disables all log output. Use the add_<*>_handler functions to complete the setup.

    This function removes any previous logging setup, also overwriting the root logger formatter.
    """

    logging.disable()

    # remove existing handlers
    if "_log.handlers" in InternalStorage:
        for handler in InternalStorage["_log.handlers"]:
            get_logger().removeHandler(handler)

            # remove atexit function
            if isinstance(handler, logging.FileHandler):
                atexit.unregister(handler.close)
                handler.close()

    if log_level is None:
        InternalStorage["_log.level"] = DEFAULT_LOG_LEVEL
        get_logger().setLevel(DEFAULT_LOG_LEVEL)
        return

    if not isinstance(log_level, (int, LogLevel)):
        raise TypeError(f"Expected log_level to be of type {int | LogLevel}, but got {type(log_level)}")

    if isinstance(log_level, LogLevel):
        log_level = log_level.value

    if log_level == LogLevel.NOTSET:
        raise ValueError("LogLevel.NOTSET is not allowed.")

    InternalStorage["_log.level"] = log_level
    get_logger().setLevel(log_level)

def add_console_handler() -> None:
    """
    Add a console handler to the root logger.

    This configures all loggers to also print to sys.stdout.
    """

    if "_log.level" not in InternalStorage:
        raise error.NotInitializedError("log.initialize() needs to be called first")

    logging.disable(0)

    stream_handler = logging.StreamHandler(sys.stdout)

    stream_handler.setLevel(InternalStorage["_log.level"])

    stream_handler.setFormatter(_get_formatter())

    get_logger().addHandler(stream_handler)

    # add logger to storage
    if "_log.handlers" not in InternalStorage:
        InternalStorage["_log.handlers"] = []
    InternalStorage["_log.handlers"].append(stream_handler)

def add_file_handler(filename: str = "latest.log") -> None:
    """
    Add a file handler to the root logger.

    This configures all loggers to also print to a given file, or 'latest.log' if not provided.
    """

    if "_log.level" not in InternalStorage:
        raise error.NotInitializedError("log.initialize() needs to be called first")

    logging.disable(0)

    file_handler = logging.FileHandler(filename=fs.absolute(filename), encoding="utf-8", mode="w", delay=True)

    file_handler.setLevel(InternalStorage["_log.level"])

    file_handler.setFormatter(_get_formatter())

    get_logger().addHandler(file_handler)

    atexit.register(file_handler.close)

    # add logger to storage
    if "_log.handlers" not in InternalStorage:
        InternalStorage["_log.handlers"] = []
    InternalStorage["_log.handlers"].append(file_handler)

def get_logger(name: str = None) -> logging.Logger:
    """
    Return a logger with the given name, or the root logger if name is None.

    If a logger doesn't yet exist, it is created and then returned.
    """

    if name is None:
        return logging.getLogger()

    if not isinstance(name, str):
        raise TypeError(f"Expected logger name to be of type {str}, but got {type(name)}")

    return logging.getLogger(name)

def get_loglevel() -> Literal[LogLevel.CRITICAL] \
                      | Literal[LogLevel.ERROR] \
                      | Literal[LogLevel.INFO] \
                      | Literal[LogLevel.WARNING] \
                      | Literal[LogLevel.DEBUG] \
                      | Literal[LogLevel.ALL] \
                      | None:
    """Return the current LogLevel"""

    return InternalStorage["_log.level"] if "_log.level" in InternalStorage else None

def _get_formatter():
    dt_fmt = r"%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    return formatter
