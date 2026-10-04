"""A module containing logger helper functions"""

from __future__ import annotations

import atexit
import logging

from abllib import error
from abllib._storage import InternalStorage
from abllib.log._log_level import LogLevel

DEFAULT_LOG_LEVEL = logging.INFO
CURRENT_LOG_LEVEL_CACHE = None

# pylint: disable=global-statement
# mypy: disable-error-code="return-value"

def initialize(log_level: LogLevel | int | None = None) -> None:
    """
    Initialize the custom logging module.

    This disables all log output. Use the add_<*>_handler functions to complete the setup.

    This function removes any previous logging setup, also overwriting the root logger formatter.
    """

    if not isinstance(log_level, (int, LogLevel)) and log_level is not None:
        raise error.WrongTypeError.with_values(log_level, int | LogLevel)

    if log_level == LogLevel.NOTSET:
        raise ValueError("LogLevel.NOTSET is not allowed.")

    if isinstance(log_level, LogLevel):
        log_level = log_level.value

    assert isinstance(log_level, int) or log_level is None

    logging.disable()
    global CURRENT_LOG_LEVEL_CACHE

    root_logger = get_logger()

    # remove existing handlers
    if "_log.handlers" in InternalStorage:
        for handler in InternalStorage["_log.handlers"]:
            root_logger.removeHandler(handler)

            # remove atexit function
            if isinstance(handler, logging.FileHandler):
                atexit.unregister(handler.close)
                handler.close()

    if log_level is None:
        InternalStorage["_log.level"] = DEFAULT_LOG_LEVEL
        root_logger.setLevel(DEFAULT_LOG_LEVEL)
        CURRENT_LOG_LEVEL_CACHE = DEFAULT_LOG_LEVEL
        return

    InternalStorage["_log.level"] = log_level
    root_logger.setLevel(log_level)
    CURRENT_LOG_LEVEL_CACHE = log_level

def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a logger with the given name, or the root logger if name is None.

    If a logger doesn't yet exist, it is created and then returned.
    """

    if name is None:
        return logging.getLogger()

    if not isinstance(name, str):
        raise error.WrongTypeError.with_values(name, str)

    return logging.getLogger(name)

def get_loglevel() -> LogLevel | None:
    """Return the current LogLevel"""

    return LogLevel(InternalStorage["_log.level"]) if "_log.level" in InternalStorage else None

def get_loglevel_fast() -> int | None:
    """
    Return the cached current LogLevel.

    The returned value can be compared to log.LogLevel.SOME_LEVEL.value

    This will be wrong if the log level was changed without calling log.initialize
    """

    return CURRENT_LOG_LEVEL_CACHE

def _setup_handler(handler: logging.Handler) -> None:
    logging.disable(0)

    handler.setLevel(InternalStorage["_log.level"])
    handler.setFormatter(_get_formatter())

    get_logger().addHandler(handler)

    # add logger to storage
    if "_log.handlers" not in InternalStorage:
        InternalStorage["_log.handlers"] = []
    InternalStorage["_log.handlers"].append(handler)

def _get_formatter() -> logging.Formatter:
    dt_fmt = r"%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    return formatter
