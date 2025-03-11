"""A module containing the logger creation"""

import atexit
import logging
import sys
from enum import Enum
from typing import Literal

from . import fs, wrapper

DEFAULT_LOG_LEVEL = logging.INFO

class LogLevel(Enum):
    """An enum holding log levels"""

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

@wrapper.singleuse
def initialize(log_level: Literal[LogLevel.CRITICAL]
                          | Literal[LogLevel.ERROR]
                          | Literal[LogLevel.WARNING]
                          | Literal[LogLevel.INFO]
                          | Literal[LogLevel.DEBUG]
                          | None = None):
    """
    Initialize the custom logging module.

    This disables all log output. Use the add_<*>_handler functions to complete the setup.

    This function can only be called once.
    """

    logging.disable()

    if log_level is None:
        get_logger().setLevel(DEFAULT_LOG_LEVEL)
        return

    if not isinstance(log_level, (int, LogLevel)):
        raise TypeError(f"Expected log_level to be of type {int | LogLevel}, but got {type(log_level)}")

    if isinstance(log_level, LogLevel):
        log_level = log_level.value

    if log_level == LogLevel.NOTSET:
        raise ValueError("LogLevel.NOTSET is not allowed.")
    if log_level == LogLevel.WARN:
        raise ValueError("LogLevel.WARN is deprecated, use LogLevel.WARNING instead.")
    if log_level == LogLevel.FATAL:
        raise ValueError("Loglevel.FATAL should not be used, use LogLevel.CRITICAL instead.")

    get_logger().setLevel(log_level)

def add_console_handler():
    """
    Add a console handler to the root logger.

    This configures all loggers to also print to sys.stdout.
    """

    logging.disable(0)

    stream_handler = logging.StreamHandler(sys.stdout)

    stream_handler.setLevel(DEFAULT_LOG_LEVEL)

    stream_handler.setFormatter(_get_formatter())

    get_logger().addHandler(stream_handler)

def add_file_handler(filename: str = "latest.log"):
    """
    Add a file handler to the root logger.

    This configures all loggers to also print to a given file, or 'latest.log' if not provided.
    """

    logging.disable(0)

    file_handler = logging.FileHandler(filename=fs.absolute(filename), encoding="utf-8", mode="w")

    file_handler.setLevel(DEFAULT_LOG_LEVEL)

    file_handler.setFormatter(_get_formatter())

    get_logger().addHandler(file_handler)

    atexit.register(file_handler.close)

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

def _get_formatter():
    dt_fmt = r"%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    return formatter
