"""A module containing an improved Enum implementation"""

from __future__ import annotations

from enum import Enum as OriginalEnum
from typing import Any

class Enum(OriginalEnum):
    """An improved Enum implementation"""

    # allow comparing Enum objects and values directly
    def __eq__(self, other: object) -> bool:
        return self is other or self.value == other

    def __ne__(self, other: object) -> bool:
        return self is not other and self.value != other

    # for more details look here:
    # https://stackoverflow.com/a/72664895/15436169
    def __hash__(self) -> int:
        return hash(self.value)

    @classmethod
    def from_name(cls, name: Any) -> Enum:
        """Return the Enum corresponding to the given name"""

        return cls[name]

    @classmethod
    def from_value(cls, value: Any) -> Enum:
        """Return the Enum corresponding to the given value"""

        return cls(value)
