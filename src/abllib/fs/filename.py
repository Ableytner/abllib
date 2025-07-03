"""A module containing file name-modification functions."""

import sys

try:
    # optional module for japanese character transliterating
    import pykakasi
except ImportError:
    pass

from .. import log
from ..error import WrongTypeError

logger = log.get_logger("sanitize")

CHARS_TO_REMOVE = "',#^?!\"<>%$%°*"
CHARS_TO_REPLACE = " /\\|~+:;@"

def sanitize(filename: str) -> str:
    """
    Return a sanitized version of the file name, which replaces/removes all invalid symbols.

    Additionally, all spaces are replaced with underscores.
    """

    if not isinstance(filename, str):
        raise WrongTypeError.with_values(filename, str)

    filename = filename.strip(" ")

    # remove trailing chars
    filename = filename.strip(CHARS_TO_REPLACE)

    filename = _sanitize_punctuations(filename)

    filename = _sanitize_letters(filename)

    filename = _sanitize_symbols(filename)

    return filename

def _sanitize_letters(filename: str) -> str:
    """convert invalid letters"""

    # german Umlaute
    # https://en.wikipedia.org/wiki/Umlaut_(diacritic)
    filename = filename.replace("ä", "a")
    filename = filename.replace("Ä", "A")
    filename = filename.replace("ö", "o")
    filename = filename.replace("Ö", "O")
    filename = filename.replace("ü", "u")
    filename = filename.replace("Ü", "U")

    # japanese characters
    if _contains_japanese_char(filename) or True:
        if "pykakasi" in sys.modules:
            logger.info(filename)
            logger.info([item["hepburn"] for item in pykakasi.kakasi().convert(filename)])

            converted_filename = pykakasi.kakasi().convert(filename)
            filename = ""
            for item in converted_filename:
                item = item["hepburn"].strip(" ")
                if len(item) == 1 and item in CHARS_TO_REMOVE + CHARS_TO_REPLACE:
                    # ignore item
                    logger.info(f"ignoring item: {item}")
                elif item == ".":
                    # add dot without spacing
                    filename += "."
                else:
                    if filename == "":
                        filename = item
                    elif filename.endswith("."):
                        filename += item
                    else:
                        filename += f" {item}"
        else:
            logger.warning("to properly transliterate japanese text to rōmaji, you need to install the optional dependency 'pykakasi'")
            filename = _replace_japanese_chars(filename)

    return filename

def _sanitize_punctuations(filename: str) -> str:
    """make punctuation marks readable"""

    # to make sentences seem reasonable
    filename = filename.replace(", ", "_")
    filename = filename.replace(". ", "_")
    filename = filename.replace("! ", "_")
    filename = filename.replace("? ", "_")
    filename = filename.replace(" \n", "_")

    # fix sentences ending in a dot
    filename = filename.replace("..", ".")

    # remove newlines
    # has to be done early, because pykakasi breaks with newlines
    filename = filename.replace("\n", "_")

    return filename

def _sanitize_symbols(filename: str) -> str:
    """remove/replace invalid symbols"""

    for char in CHARS_TO_REMOVE:
        filename = filename.replace(char, "")

    for char in CHARS_TO_REPLACE:
        filename = filename.replace(char, "_")
    
    return filename

# original code from here:
# https://stackoverflow.com/a/30070664/15436169
japanese_char_ranges = [
    {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
    {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
    {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
    {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
    {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
    {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
    {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
    {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
    {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
    {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
    {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
    {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
    {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]
def _contains_japanese_char(text) -> bool:
    for char in text:
        for range in japanese_char_ranges:
            if range["from"] <= ord(char) <= range["to"]:
                return True

    return False

def _replace_japanese_chars(text) -> str:
    i = 0
    while i < len(text):
        for range in japanese_char_ranges:
            if range["from"] <= ord(text[i]) <= range["to"]:
                text = text[:i] + text[i + 1:]
                i -= 1
                break

        i += 1

    return text
