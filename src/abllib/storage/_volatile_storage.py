"""Module containing the _VolatileStorage class"""

from .._storage._base_storage import _BaseStorage
from ..storage._storage_view import _StorageView
from .. import error, wrapper

class _VolatileStorage(_BaseStorage):
    """Storage that is not saved across restarts"""

    def __init__(self) -> None:
        if _VolatileStorage._instance is not None:
            raise error.SingletonInstantiationError.with_values(_VolatileStorage)

        _VolatileStorage._instance = self

    def initialize(self):
        """
        Initialize only the VolatileStorage.

        Not needed if you already called abllib.storage.initialize().
        """

        if _VolatileStorage._store is not None:
            # this is a re-initialization
            return

        _VolatileStorage._store = self._store = {}

        # we cannot use StorageView defined in __init__.py because of circular imports
        # pylint: disable-next=protected-access
        _StorageView._instance.add_storage(self)

    _LOCK_NAME = "_VolatileStorage"

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def contains_item(self, key, item):
        return super().contains_item(key, item)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def contains(self, key):
        return super().contains(key)

    @wrapper.NamedLock(_LOCK_NAME)
    def pop(self, key):
        return super().pop(key)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def __getitem__(self, key):
        return super().__getitem__(key)

    @wrapper.NamedLock(_LOCK_NAME)
    def __setitem__(self, key, item):
        return super().__setitem__(key, item)

    @wrapper.NamedLock(_LOCK_NAME)
    def __delitem__(self, key):
        return super().__delitem__(key)

    @wrapper.NamedSemaphore(_LOCK_NAME)
    def __contains__(self, key):
        return super().__contains__(key)

    def _ensure_initialized(self):
        try:
            super()._ensure_initialized()
        except error.NotInitializedError as exc:
            raise error.NotInitializedError("VolatileStorage is not yet initialized, "
                                            + "are you sure you called storage.initialize() "
                                            + "or VolatileStorage.initialize()?") \
                                           from exc
