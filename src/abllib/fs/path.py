"""A module containing path-modification functions."""

import pathlib

from abllib.error import WrongTypeError

def absolute(*paths: str | pathlib.Path) -> str:
    """
    Return an absolute path, regardless of what is input.

    Additionally, the path is resolved, removing any symlinks on the way.
    """

    paths_list = list(paths)

    if len(paths_list) == 0:
        raise ValueError()
    for item in paths_list:
        if not isinstance(item, (str, pathlib.Path)):
            raise WrongTypeError().with_values(item, (str, pathlib.Path))

    if isinstance(paths_list[0], str):
        if paths_list[0] == "~":
            paths_list[0] = pathlib.Path.home()
        elif paths_list[0].startswith("~/"):
            paths_list[0] = paths_list[0].replace("~", str(pathlib.Path.home()), 1)

    path = pathlib.Path(*paths_list)

    return str(path.absolute().resolve())
