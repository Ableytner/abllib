"""A module containing file name-modification functions."""

from ..error import WrongTypeError

def sanitize(filename: str) -> str:
    """
    Return a sanitized version of the file name, which removes all invalid symbols.

    Additionally, all spaces are replaced with underscores.
    """

    if not isinstance(filename, str): raise WrongTypeError.with_values(filename, str)

    chars_to_remove = "',#^?!\"<>%$%°*"
    chars_to_replace = " /\\|~+:;"

    # to make sentences seem reasonable
    filename = filename.replace(", ", "_")
    filename = filename.replace(". ", "_")
    filename = filename.replace("! ", "_")
    filename = filename.replace("? ", "_")

    for char in chars_to_remove:
        filename = filename.replace(char, "")
    
    for char in chars_to_replace:
        filename = filename.replace(char, "_")

    return filename
