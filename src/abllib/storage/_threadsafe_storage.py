"""Module containing the _PersistentStorage class"""

from typing import Any

from .._storage._base_storage import _BaseStorage
from .. import wrapper

class _ThreadsafeStorage(_BaseStorage):
    def __init__(self):
        raise NotImplementedError()

    _LOCK_NAME = "_ThreadsafeStorage"

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def contains_item(self, key, item):
        return super().contains_item(key, item)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def contains(self, key):
        return super().contains(key)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def items(self):
        return super().items()

    @wrapper.NamedLock(_LOCK_NAME)
    def pop(self, key) -> Any:
        return super().pop(key)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def keys(self):
        return super().keys()

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def values(self):
        return super().values()

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def __getitem__(self, key):
        return super().__getitem__(key)

    @wrapper.NamedLock(_LOCK_NAME)
    def __setitem__(self, key: str, item: Any) -> None:
        return super().__setitem__(key, item)

    @wrapper.NamedLock(_LOCK_NAME)
    def __delitem__(self, key):
        return super().__delitem__(key)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def __contains__(self, key):
        return super().__contains__(key)
