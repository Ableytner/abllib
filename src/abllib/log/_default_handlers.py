"""A module containing the default log handlers"""

from __future__ import annotations

import atexit
import logging
import sys
from typing import Literal

from abllib import error
from abllib._storage import InternalStorage
from abllib.log._helpers import _setup_handler

def add_console_handler() -> None:
    """
    Add a console handler to the root logger.

    This configures all loggers to also print to sys.stdout.
    """

    if "_log.level" not in InternalStorage:
        raise error.NotInitializedError("log.initialize() needs to be called first")

    stream_handler = logging.StreamHandler(sys.stdout)

    _setup_handler(stream_handler)

def add_file_handler(filename: str = "latest.log", filemode: Literal["w"] | Literal["a"] = "w") -> None:
    """
    Add a file handler to the root logger.

    This configures all loggers to also print to a given file, or 'latest.log' if not provided.
    """

    if "_log.level" not in InternalStorage:
        raise error.NotInitializedError("log.initialize() needs to be called first")

    # needs to be imported here to prevent circular import
    # pylint: disable-next=cyclic-import, import-outside-toplevel
    from abllib.fs import absolute
    file_handler = logging.FileHandler(filename=absolute(filename), encoding="utf-8", mode=filemode, delay=True)

    atexit.register(file_handler.close)

    _setup_handler(file_handler)
