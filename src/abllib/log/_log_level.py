"""A module containing the LogLevel enum"""

from __future__ import annotations

import logging

from abllib import error
from abllib.enum import Enum

class LogLevel(Enum):
    """An enum holding log levels"""

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    ALL = 1
    NOTSET = logging.NOTSET

    @staticmethod
    def from_str(log_level: str) -> LogLevel:
        """Return the matching LogLevel enum value from the given string"""

        match log_level.lower():
            case "all":
                return LogLevel.ALL
            case "debug":
                return LogLevel.DEBUG
            case "info":
                return LogLevel.INFO
            case "warning":
                return LogLevel.WARNING
            case "error":
                return LogLevel.ERROR
            case "critical":
                return LogLevel.CRITICAL
            case _:
                raise error.NameNotFoundError(f"'{log_level}' isn't a known log level")
