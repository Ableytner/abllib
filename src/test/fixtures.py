"""
    Pytest fixtures
"""

# pylint: disable=protected-access, missing-class-docstring

import atexit
import os
import shutil

import pytest

from abllib import fs, log, storage, _storage

logger = log.get_logger("test")

@pytest.fixture(scope="session", autouse=True)
def setup():
    """Setup the PersistentStorage, VolatileStorage and StorageView for test usage"""

    # setup testing dirs
    STORAGE_DIR = fs.absolute(os.path.dirname(__file__), "..", "..", "test_run")
    shutil.rmtree(STORAGE_DIR, ignore_errors=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)

    #  setup logging
    log.initialize(log.LogLevel.DEBUG)
    log.add_console_handler()
    log.add_file_handler(os.path.join(STORAGE_DIR, "test.log"))

    STORAGE_FILE = fs.absolute(STORAGE_DIR, "test.json")

    if os.path.isfile(STORAGE_FILE):
        os.remove(STORAGE_FILE)

    storage.initialize(STORAGE_FILE)

    # disable atexit storage saving
    atexit.unregister(storage.PersistentStorage.save_to_disk)

    yield None

    storage.PersistentStorage.save_to_disk()

@pytest.fixture(scope="function", autouse=True)
def clean_after_function():
    """Clean up the PersistentStorage, VolatileStorage and StorageView, removing all keys"""

    yield None

    for key in list(storage.PersistentStorage._store.keys()):
        del storage.PersistentStorage[key]

    for key in list(storage.VolatileStorage._store.keys()):
        if key not in ["storage_file"]:
            del storage.VolatileStorage[key]

    for key in list(_storage.InternalStorage._store.keys()):
        del _storage.InternalStorage[key]
