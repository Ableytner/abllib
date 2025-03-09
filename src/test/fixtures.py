"""
    Pytest fixtures
"""

# pylint: disable=protected-access, missing-class-docstring

import atexit
import os

import pytest

from abllib import log, storage

logger = log.get_logger("test")

@pytest.fixture(scope="function", autouse=True)
def setup_storages():
    """Setup the PersistentStorage, VolatileStorage and StorageView for test usage"""

    storage.initialize("test.json")

    # disable atexit storage saving
    atexit.unregister(storage.PersistentStorage.save_to_disk)

    yield None

    os.remove("test.json")
