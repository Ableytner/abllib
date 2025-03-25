"""Module containing the _PersistentStorage class"""

# pylint: disable=protected-access

import json
import os
from typing import Any

from .._storage._base_storage import _BaseStorage
from ._volatile_storage import _VolatileStorage
from .. import error, wrapper

class _PersistentStorage(_BaseStorage):
    """Storage that is persistent across restarts"""

    def __init__(self) -> None:
        pass

    def _init(self):
        if _PersistentStorage._instance is not None:
            raise error.SingletonInstantiationError()

        _PersistentStorage._store = self._store = {}
        _PersistentStorage._instance = self

    _LOCK_NAME = "_PersistentStorage"

    @wrapper.ReadLock(_LOCK_NAME)
    def contains_item(self, key, item):
        return super().contains_item(key, item)

    @wrapper.ReadLock(_LOCK_NAME)
    def contains(self, key):
        return super().contains(key)

    @wrapper.WriteLock(_LOCK_NAME)
    def pop(self, key) -> Any:
        return super().pop(key)

    @wrapper.ReadLock(_LOCK_NAME)
    def __getitem__(self, key):
        return super().__getitem__(key)

    @wrapper.WriteLock(_LOCK_NAME)
    def __setitem__(self, key: str, item: Any) -> None:
        if not isinstance(item, (str, int, list, dict)):
            raise TypeError(f"Tried to add item with type {type(item)} to PersistentStorage")

        return super().__setitem__(key, item)

    @wrapper.WriteLock(_LOCK_NAME)
    def __delitem__(self, key):
        return super().__delitem__(key)

    @wrapper.ReadLock(_LOCK_NAME)
    def __contains__(self, key):
        return super().__contains__(key)

    def load_from_disk(self) -> None:
        """Load the data from the storage file"""

        if "storage_file" not in _VolatileStorage._instance:
            raise error.KeyNotFoundError()

        path = _VolatileStorage._instance["storage_file"]
        if not os.path.isfile(path):
            return

        with open(path, "r", encoding="utf8") as f:
            self._store = json.load(f)

    def save_to_disk(self) -> None:
        """Save the data to the storage file"""

        if "storage_file" not in _VolatileStorage._instance:
            raise error.KeyNotFoundError()

        path = _VolatileStorage._instance["storage_file"]
        if len(self._store) == 0 and os.path.isfile(path):
            return

        with open(path, "w", encoding="utf8") as f:
            json.dump(self._store, f)

    def _ensure_initialized(self):
        try:
            super()._ensure_initialized()
        except error.NotInitializedError as exc:
            raise error.NotInitializedError("PersistentStorage is not yet initialized, "
                                            + "are you sure you called storage.initialize()?") \
                                           from exc
