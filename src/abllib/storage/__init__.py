"""A module containing json-like storages"""

from .._storage import _base_storage, _internal_storage
from ._cache_storage import _CacheStorage
from ._persistent_storage import _PersistentStorage
from ._volatile_storage import _VolatileStorage
from ._storage_view import _StorageView

# pylint: disable=protected-access

def initialize(filename: str = "storage.json", save_on_exit: bool = False):
    """
    Initialize the storage module.

    If save_on_exit is set to True, automatically calls PersistentStorage.save_to_disk on application exit.
    """

    VolatileStorage.initialize()
    StorageView.add_storage(VolatileStorage)

    PersistentStorage.initialize(filename, save_on_exit)
    StorageView.add_storage(PersistentStorage)

VolatileStorage = _VolatileStorage()
PersistentStorage = _PersistentStorage()
CacheStorage = _CacheStorage()
StorageView = _StorageView()
StorageView._init()

__exports__ = [
    initialize,
    VolatileStorage,
    PersistentStorage,
    CacheStorage,
    StorageView,
    _base_storage,
    _internal_storage
]
