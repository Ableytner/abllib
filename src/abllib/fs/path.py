"""A module containing path-modification functions."""

import pathlib

def absolute(path: str | pathlib.Path, *paths: str) -> str:
    """
    Return an absolute path, regardless of what is input.

    Additionally, the path is resolved, removing any symlinks on the way.
    """

    if not isinstance(path, (str, pathlib.Path)):
        raise TypeError()

    if isinstance(path, str):
        if len(paths) > 0:
            path = pathlib.Path(path, *paths)
        else:
            path = pathlib.Path(path)

    if path.is_absolute():
        return str(path.resolve())

    return str(path.absolute().resolve())
