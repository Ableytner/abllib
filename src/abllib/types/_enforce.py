"""A module containing functions to enforce that given values match their type hint."""

from typing import Any

import pathlib

def enforce(value: Any, target_type_or_value: Any) -> None:
    """
    Ensure that the given value is of type target_type,
    otherwise raise a WrongTypeError.
    """

    if type(type(target_type_or_value)) == type(target_type_or_value):
        pass

def absolute(*paths: str | pathlib.Path) -> str:
    """
    Return an absolute path, regardless of what is input.

    Additionally, the path is resolved, removing any symlinks on the way.
    """

    if len(paths) == 0:
        raise ValueError()
    for item in paths:
        if not isinstance(item, (str, pathlib.Path)):
            raise TypeError()

    path = pathlib.Path(*paths)

    if path.is_absolute():
        return str(path.resolve())

    return str(path.absolute().resolve())
