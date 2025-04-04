"""Module containing the _StorageView class"""

# pylint: disable=protected-access

import functools
from typing import Any

from .._storage._base_storage import _BaseStorage
from .. import error, wrapper

def _locking(func):
    """Make a function require all storage locks to be held"""

    @functools.wraps(func)
    def inner(*args, **kwargs):
        """The wrapped function that is called on function execution"""

        self: _StorageView = args[0]

        for storage in self._storages:
            lock = wrapper.ReadLock(storage._LOCK_NAME)
            lock.acquire()

        try:
            return func(*args, **kwargs)
        finally:
            for storage in self._storages:
                lock = wrapper.ReadLock(storage._LOCK_NAME)
                lock.release()

    return inner

class _StorageView():
    """A read-only view on both the PersistentStorage and VolatileStorage"""

    def __init__(self):
        pass

    def _init(self, storages: list[_BaseStorage]):
        for storage in storages:
            if not isinstance(storage, _BaseStorage):
                raise error.MissingInheritanceError.with_values(storage, _BaseStorage)
            self._storages.append(storage)

    _storages: list[_BaseStorage] = []

    @_locking
    def contains_item(self, key: str, item: Any) -> bool:
        """
        Checks whether a key within the storage equals an item
        If 'key' contains a '.', also checks if all sub-dicts exist
        """

        for storage in self._storages:
            if storage.contains_item(key, item):
                return True
        return False

    @_locking
    def contains(self, key: str) -> bool:
        """
        Checks whether a key exists within the storage
        If 'key' contains a '.', also checks if all sub-dicts exist
        """

        for storage in self._storages:
            if storage.contains(key):
                return True
        return False

    @_locking
    def __getitem__(self, key: str) -> Any:
        for storage in self._storages:
            if key in storage:
                return storage[key]
        raise error.KeyNotFoundError.with_values(key)

    @_locking
    def __contains__(self, key: str) -> bool:
        return self.contains(key)
