"""Module containing the _VolatileStorage class"""

from .._storage._base_storage import _BaseStorage
from .. import error

class _VolatileStorage(_BaseStorage):
    """Storage that is not saved across restarts"""

    def __init__(self) -> None:
        pass

    def _init(self):
        if _VolatileStorage._instance is not None:
            raise error.SingletonInstantiationError()

        _VolatileStorage._store = self._store = {}
        _VolatileStorage._instance = self
