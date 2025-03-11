"""
    Pytest fixtures
"""

# pylint: disable=protected-access, missing-class-docstring

import atexit
import os

import pytest

from abllib import fs, log, storage

logger = log.get_logger("test")

@pytest.fixture(scope="session", autouse=True)
def setup_storages():
    """Setup the PersistentStorage, VolatileStorage and StorageView for test usage"""

    STORAGE_FILE = fs.absolute(os.path.dirname(__file__), "..", "..", "test_run", "test.json")

    if os.path.isfile(STORAGE_FILE):
        os.remove(STORAGE_FILE)

    storage.initialize(STORAGE_FILE)

    # disable atexit storage saving
    atexit.unregister(storage.PersistentStorage.save_to_disk)

    yield None

@pytest.fixture(scope="function", autouse=True)
def clean_storages():
    """Clean up the PersistentStorage, VolatileStorage and StorageView, removing all keys"""

    yield None

    for key in storage.PersistentStorage._store.keys():
        del storage.PersistentStorage[key]

    for key in storage.VolatileStorage._store.keys():
        if key not in ["storage_file"]:
            del storage.VolatileStorage[key]
