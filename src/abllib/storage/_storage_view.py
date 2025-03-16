"""Module containing the _StorageView class"""

from typing import Any

from .._storage._base_storage import _BaseStorage
from .. import error

class _StorageView():
    """A read-only view on both the PersistentStorage and VolatileStorage"""

    def __init__(self):
        pass

    def _init(self, storages: list[_BaseStorage]):
        for storage in storages:
            if not isinstance(storage, _BaseStorage):
                raise error.MissingInheritanceError(f"Storage {type(storage)} does not inherit from _BaseStorage")
            self._storages.append(storage)

    _storages = []

    def contains_item(self, key: str, item: Any) -> bool:
        """
        Checks whether a key within the storage contains an item
        If 'key' contains a '.', also checks if all sub-dicts exist
        """

        for storage in self._storages:
            if storage.contains_item(key, item):
                return True
        return False

    def contains(self, key: str) -> bool:
        """
        Checks whether a key exists within the storage
        If 'key' contains a '.', also checks if all sub-dicts exist
        """

        for storage in self._storages:
            if storage.contains(key):
                return True
        return False

    def __getitem__(self, key: str) -> Any:
        for storage in self._storages:
            if key in storage:
                return storage[key]
        raise error.KeyNotFoundError(f"Key '{key}' not found in storage")

    def __contains__(self, key: str) -> bool:
        return self.contains(key)
