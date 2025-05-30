"""Module containing the _CacheStorage class"""

from .._storage._base_storage import _BaseStorage
from .. import error

class _CacheStorage(_BaseStorage):
    """Storage used for caching values at runtime"""

    def __init__(self) -> None:
        if _CacheStorage._instance is not None:
            raise error.SingletonInstantiationError.with_values(_CacheStorage)

        _CacheStorage._instance = self
        _CacheStorage._store = self._store = {}

    def contains_item(self, key, item):
        return super().contains_item(key, item)

    def contains(self, key):
        return super().contains(key)

    def pop(self, key):
        return super().pop(key)

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, item):
        return super().__setitem__(key, item)

    def __delitem__(self, key):
        return super().__delitem__(key)

    def __contains__(self, key):
        return super().__contains__(key)

    def _ensure_initialized(self):
        return True
