"""Module containing the _PersistentStorage class"""

import base64
import json
import os
from typing import Any

from abllib import error, fs, onexit, wrapper
from abllib._storage import InternalStorage
from abllib._storage._base_storage import _AutoremoveDict
from abllib.storage._storage_view import _StorageView
from abllib.storage._threadsafe_storage import _ThreadsafeStorage

# pylint: disable=protected-access
# mypy: ignore-errors

class _PersistentStorage(_ThreadsafeStorage):
    """Storage that persists across restarts"""

    def __init__(self) -> None:
        if _PersistentStorage._instance is not None:
            raise error.SingletonInstantiationError.with_values(_PersistentStorage)

        _PersistentStorage._instance = self

    def initialize(self, filename: str = "storage.json", save_on_exit: bool = False):
        """
        Initialize only the PersistentStorage.

        Not needed if you already called abllib.storage.initialize().

        If save_on_exit is set to True, automatically calls save_to_disk on application exit.
        """

        full_filepath = fs.absolute(filename)
        if not os.path.isdir(os.path.dirname(full_filepath)):
            raise error.DirNotFoundError.with_values(os.path.dirname(full_filepath))

        if _PersistentStorage._store is not None:
            # this is a re-initialization
            if save_on_exit:
                try:
                    onexit.register("PersistentStorage.save", self.save_to_disk)
                except error.RegisteredMultipleTimesError:
                    pass
            else:
                try:
                    onexit.deregister("PersistentStorage.save")
                except error.NameNotFoundError:
                    pass

            if InternalStorage.contains_item("_storage_file", full_filepath):
                # the storage file didn't change
                pass
            else:
                # the storage file changed
                # save current store to old file
                self.save_to_disk()

                InternalStorage["_storage_file"] = full_filepath
                self.load_from_disk()

            return

        _PersistentStorage._store = self._store = {}

        _StorageView._instance.add_storage(self)

        InternalStorage["_storage_file"] = full_filepath
        self.load_from_disk()

        if save_on_exit:
            onexit.register("PersistentStorage.save", self.save_to_disk)

    _STORAGE_NAME = "PersistentStorage"

    def __setitem__(self, key: str, item: Any) -> None:
        # TODO: type check list / dict content types

        if not isinstance(item, (bool, int, float, str, list, dict, tuple, bytes)) and item is not None:
            raise TypeError(f"Tried to add item with type {type(item)} to PersistentStorage")

        return super().__setitem__(key, item)

    @wrapper.NamedLock(_STORAGE_NAME)
    def save_to_disk(self) -> None:
        """Save the data to the storage file"""

        if "_storage_file" not in InternalStorage:
            raise error.KeyNotFoundError()

        path = InternalStorage["_storage_file"]
        if len(self._store) == 0 and os.path.isfile(path):
            return

        data = {}
        for key in self._store.keys():
            data[key] = self._encode_data(self._store[key])

        with open(path, "w", encoding="utf8") as f:
            json.dump(data, f)

    @wrapper.NamedLock(_STORAGE_NAME)
    def load_from_disk(self) -> None:
        """Load the data from the storage file"""

        if "_storage_file" not in InternalStorage:
            raise error.KeyNotFoundError()

        path = InternalStorage["_storage_file"]
        if not os.path.isfile(path):
            return

        with open(path, "r", encoding="utf8") as f:
            data = json.load(f)

        self._store = {}
        for key in data.keys():
            self._store[key] = self._decode_data(data[key])

    def _encode_data(self, data: Any) -> Any:
        """Encode the given data item, replacing all type / value combinations"""

        item = data
        if isinstance(item, dict):
            if isinstance(item, _AutoremoveDict):
                item = {
                    "_t": "_AutoremoveDict",
                    "_v": {key: self._encode_data(item[key]) for key in item}
                }
            else:
                item = {
                    "_t": "dict",
                    "_v": {key: self._encode_data(item[key]) for key in item}
                }
        elif isinstance(item, list):
            item = {
                "_t": "list",
                "_v": [self._encode_data(i) for i in item]
            }
        elif isinstance(item, tuple):
            item = {
                "_t": "tuple",
                "_v": [self._encode_data(i) for i in item]
            }
        elif isinstance(item, bytes):
            item = {
                "_t": "bytes",
                "_v": base64.b64encode(item).decode("ascii")
            }

        return item

    def _decode_data(self, data: Any) -> Any:
        """Decode the given data item, replacing all type / value combinations"""

        if not isinstance(data, dict):
            return data

        if len(data) == 2 and "_t" in data and "_v" in data:
            if data["_t"] == "_AutoremoveDict":
                data = _AutoremoveDict({key: self._decode_data(item) for key, item in data["_v"].items()})
            elif data["_t"] == "dict":
                data = {key: self._decode_data(item) for key, item in data["_v"].items()}
            elif data["_t"] == "list":
                data = [self._decode_data(i) for i in (data["_v"])]
            elif data["_t"] == "tuple":
                data = tuple(self._decode_data(i) for i in (data["_v"]))
            elif data["_t"] == "bytes":
                data = base64.b64decode(data["_v"], validate=True)

            return data

        # handle legacy format, which doesn't need any conversion
        return data

    def _ensure_initialized(self):
        try:
            super()._ensure_initialized()
        except error.NotInitializedError as exc:
            raise error.NotInitializedError("PersistentStorage is not yet initialized, "
                                            + "are you sure you called storage.initialize()?") \
                                           from exc
