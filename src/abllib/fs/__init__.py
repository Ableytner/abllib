"""A module containing file system-related functionality"""

from abllib.fs.filename import sanitize as sanitize
from abllib.fs.path import absolute as absolute

__exports__ = [
    absolute,
    sanitize
]
