"""Module containing the _BaseStorage base class"""

from __future__ import annotations

from typing import Any

from .. import error

class _BaseStorage():
    def __init__(self) -> None:
        raise NotImplementedError()

    _instance: _BaseStorage = None
    _store: dict[str, Any] = None

    _LOCK_NAME = "_BaseStorage"

    def contains_item(self, key: str, item: Any) -> bool:
        """
        Check whether a key within the storage equals an item.

        If 'key' contains a '.', also checks if all sub-dicts exist.
        """

        if not isinstance(key, str):
            raise TypeError()

        if not self._contains(key):
            return False
        return item == self[key]

    def contains(self, key: str) -> bool:
        """
        Check whether a key exists within the storage.

        If 'key' contains a '.', also checks if all sub-dicts exist.
        """

        return self._contains(key)

    def pop(self, key: str) -> Any:
        """
        Return the value of an key if it exists in the storage.
        """

        val = self._get(key)
        self._del(key)
        return val

    def __getitem__(self, key: str) -> Any:
        return self._get(key)

    def __setitem__(self, key: str, item: Any) -> None:
        return self._set(key, item)

    def __delitem__(self, key: str) -> None:
        return self._del(key)

    def __contains__(self, key: str) -> bool:
        return self._contains(key)

    def __str__(self) -> str:
        return str(self._store)

    def _ensure_initialized(self) -> None:
        if self._store is None:
            raise error.NotInitializedError()

    def _contains(self, key: str) -> bool:
        self._ensure_initialized()

        if not isinstance(key, str):
            raise TypeError()

        if "." not in key:
            return key in self._store

        parts = key.split(".")
        curr_dict: dict[str, Any] = self._store
        for c, part in enumerate(parts):
            if part not in curr_dict:
                return False
            # if it isn't the last part
            if c < len(parts) - 1:
                curr_dict: dict[str, Any] = curr_dict[part]

        return parts[-1] in curr_dict

    def _get(self, key: str) -> Any:
        self._ensure_initialized()

        if not isinstance(key, str):
            raise TypeError()

        if "." not in key:
            if key not in self._store:
                raise error.KeyNotFoundError(f"Key '{key}' not found in storage")
            return self._store[key]

        parts = key.split(".")
        curr_dict = self._store
        for c, part in enumerate(parts):
            if part not in curr_dict:
                invalid_key = ""
                for item in parts:
                    invalid_key += f"{item}" if invalid_key == "" else f".{item}"
                    if item == part:
                        break
                raise error.KeyNotFoundError(f"Key '{invalid_key}' not found in storage")
            # if it isn't the last part
            if c < len(parts) - 1:
                curr_dict = curr_dict[part]

        return curr_dict[parts[-1]]

    def _set(self, key: str, item: Any) -> None:
        self._ensure_initialized()

        if not isinstance(key, str):
            raise TypeError()

        if "." not in key:
            self._store[key] = item
            return

        parts = key.split(".")
        curr_dict = self._store
        for c, part in enumerate(parts):
            # if it isn't the last part
            if c < len(parts) - 1:
                # add a missing dictionary
                if part not in curr_dict:
                    curr_dict[part] = {}
                curr_dict = curr_dict[part]
            else:
                # add the actual item
                curr_dict[part] = item

    def _del(self, key: str) -> None:
        self._ensure_initialized()

        if not isinstance(key, str):
            raise TypeError()

        if "." not in key:
            if key not in self._store:
                raise error.KeyNotFoundError(f"Key '{key}' not found in storage")
            del self._store[key]
            return

        parts = key.split(".")
        curr_dict = self._store
        for c, part in enumerate(parts):
            if part not in curr_dict:
                invalid_key = ""
                for item in parts:
                    invalid_key += f"{item}" if invalid_key == "" else f".{item}"
                    if item == part:
                        break
                raise error.KeyNotFoundError(f"Key '{invalid_key}' not found in storage")

            # if it isn't the last part
            if c < len(parts) - 1:
                curr_dict = curr_dict[part]
            else:
                # delete the actual item
                del curr_dict[part]
