"""Module containing the _InternalStorage class"""

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

InternalStorage = _InternalStorage()
# pylint: disable-next=protected-access
InternalStorage._init()
