"""A module containing json-like storages"""

import atexit

from .._storage import _base_storage, _internal_storage
from ._persistent_storage import _PersistentStorage
from ._volatile_storage import _VolatileStorage
from ._storage_view import _StorageView
from .. import wrapper

# pylint: disable=protected-access

@wrapper.singleuse
def initialize(filename: str = "storage.json"):
    """
    Initialize the storage module.

    This function can only be called once.
    """

    VolatileStorage.initialize()
    StorageView.add_storage(VolatileStorage)

    PersistentStorage.initialize(filename)
    StorageView.add_storage(PersistentStorage)

    # save persistent storage before program exits
    atexit.register(PersistentStorage.save_to_disk)

VolatileStorage = _VolatileStorage()
PersistentStorage = _PersistentStorage()
StorageView = _StorageView()
StorageView._init()

__exports__ = [
    initialize,
    VolatileStorage,
    PersistentStorage,
    StorageView,
    _base_storage,
    _internal_storage
]
