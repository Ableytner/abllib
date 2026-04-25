"""Module containing tests for the abllib.convert module"""

import pytest

from abllib import convert
from abllib.error import WrongTypeError

# pylint: disable=missing-class-docstring

def test_as_time():
    """Ensure that convert.as_time works as expected"""

    assert callable(convert.as_time)
    assert convert.as_time(0.000072) == "72.0μs"
    assert convert.as_time(0.0072) == "7.2ms"
    assert convert.as_time(10) == "10.0s"
    assert convert.as_time(1000) == "16.7min"
    assert convert.as_time(1000.00) == "16.7min"
    assert convert.as_time(7200) == "2.0h"
    assert convert.as_time(86000) == "23.9h"
    assert convert.as_time(100000) == "1.2d"
    assert convert.as_time(30000000) == "347.2d"
    assert convert.as_time(300000000) == "9.5y"

    with pytest.raises(WrongTypeError):
        convert.as_time(None)
    with pytest.raises(WrongTypeError):
        convert.as_time("test")
    with pytest.raises(WrongTypeError):
        convert.as_time("1")
    with pytest.raises(WrongTypeError):
        convert.as_time([1, 2])

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
