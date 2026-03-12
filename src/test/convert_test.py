"""Module containing tests for the abllib.convert module"""

import pytest

from abllib import convert
from abllib.error import WrongTypeError

# pylint: disable=missing-class-docstring

def test_as_bytes():
    """Ensure that convert.as_bytes works as expected"""

    assert callable(convert.as_bytes)
    assert convert.as_bytes(1000) == "1.0kB"
    assert convert.as_bytes(1000.00) == "1.0kB"
    assert convert.as_bytes(12345678) == "12.3MB"
    assert convert.as_bytes(9876543219876) == "9.9TB"

    with pytest.raises(WrongTypeError):
        convert.as_bytes(None)
    with pytest.raises(WrongTypeError):
        convert.as_bytes("test")
    with pytest.raises(WrongTypeError):
        convert.as_bytes("1")
    with pytest.raises(WrongTypeError):
        convert.as_bytes([1, 2])

def test_get_bytes():
    """Ensure that convert.get_bytes works as expected"""

    assert callable(convert.get_bytes)
    assert convert.get_bytes("1.0kB") == 1000
    assert convert.get_bytes("12.3MB") == 12300000
    assert convert.get_bytes("9.9TB") == 9900000000000

    with pytest.raises(WrongTypeError):
        convert.get_bytes(None)
    with pytest.raises(WrongTypeError):
        convert.get_bytes(10)
    with pytest.raises(WrongTypeError):
        convert.get_bytes([1, 2])
    with pytest.raises(ValueError):
        convert.get_bytes("test")
    with pytest.raises(ValueError):
        convert.get_bytes("1a2.3B")
