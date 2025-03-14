"""A module containing json-like storages"""

# pylint: disable=protected-access

import atexit
import os

from . import _base_storage, _internal_storage
from ._persistent_storage import _PersistentStorage
from ._volatile_storage import _VolatileStorage
from ._storage_view import _StorageView
from .. import error, fs, wrapper

@wrapper.singleuse
def initialize(filename: str = "storage.json"):
    """
    Initialize the storage module.

    This function can only be called once.
    """

    full_filepath = fs.absolute(filename)
    if not os.path.isdir(os.path.dirname(full_filepath)):
        raise error.DirNotFoundError()

    VolatileStorage._init()
    PersistentStorage._init()
    StorageView._init([VolatileStorage, PersistentStorage])

    VolatileStorage["storage_file"] = full_filepath

    PersistentStorage.load_from_disk()

    # save persistent storage before program exits
    atexit.register(PersistentStorage.save_to_disk)

VolatileStorage = _VolatileStorage()
PersistentStorage = _PersistentStorage()
StorageView = _StorageView()

__exports__ = [
    initialize,
    VolatileStorage,
    PersistentStorage,
    StorageView,
    _base_storage,
    _internal_storage
]
