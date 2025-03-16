"""Module containing the _InternalStorage class"""

from typing import Any

from ._base_storage import _BaseStorage
from .. import error

class _InternalStorage(_BaseStorage):
    """Internal storage that is not saved across restarts"""

    def __init__(self) -> None:
        pass

    def _init(self):
        if _InternalStorage._instance is not None:
            raise error.SingletonInstantiationError()

        _InternalStorage._store = self._store = {}
        _InternalStorage._instance = self

    def __setitem__(self, key: str, item: Any) -> None:
        if not key.startswith("_"):
            raise error.InternalFunctionUsedError("Please use storage.VolatileStorage instead")

        return super().__setitem__(key, item)
