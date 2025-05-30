"""Module containing tests for the abllib.types module"""

# pylint: disable=missing-class-docstring, unused-argument

import pytest

from abllib import types
from abllib.error import WrongTypeError

def test_enforce():
    """Ensure that fs.enforce works as expected"""

    assert callable(types.enforce)

    types.enforce("test", str)

    types.enforce(0, int)
    types.enforce(-35752, int)

    types.enforce(2.8, float)

    types.enforce(None, None)

    class MyClass:
        pass
    types.enforce(MyClass(), MyClass)

    types.enforce([1, 2, 3], list)

    types.enforce({"key": "val"}, dict)

def test_enforce_wronginput():
    """Ensure that fs.enforce checks for valid input types"""

    try:
        types.enforce("test", "another")
    except WrongTypeError as exc:
        assert "Expected target_type to be a valid type" in str(exc)

def test_enforce_wrongtypes():
    """Ensure that fs.enforce works as expected"""

    with pytest.raises(WrongTypeError):
        types.enforce("test", int)

    with pytest.raises(WrongTypeError):
        types.enforce(0, str)
    with pytest.raises(WrongTypeError):
        types.enforce(-35752, float)
    with pytest.raises(WrongTypeError):
        types.enforce(999999, None)

    with pytest.raises(WrongTypeError):
        types.enforce(2.8, int)

    with pytest.raises(WrongTypeError):
        types.enforce(None, str)

    class MyClass:
        pass
    with pytest.raises(WrongTypeError):
        types.enforce(MyClass(), None)
    with pytest.raises(WrongTypeError):
        types.enforce(None, MyClass)
    with pytest.raises(WrongTypeError):
        types.enforce(MyClass(), str)

    with pytest.raises(WrongTypeError):
        types.enforce([1, 2, 3], int)

    with pytest.raises(WrongTypeError):
        types.enforce({"key": "val"}, str)

def test_enforce_wrapper():
    """Ensure that fs.enforce wraps a function as expected"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str, val2: int, val3: float = 0.1, val4: int = -9999):
        return str(val2)

    assert myfunc("test", 187) == "187"
    assert myfunc("test", 187, -35.35) == "187"
    assert myfunc("test", 187, val3=-35.35) == "187"
    assert myfunc("test", 187, 15346.0, val4=42) == "187"
    assert myfunc("test", 187, val4=42) == "187"

    with pytest.raises(WrongTypeError):
        myfunc("test", "187")
    with pytest.raises(WrongTypeError):
        myfunc(1, 187)
    with pytest.raises(WrongTypeError):
        myfunc("test", 187, "test2")
    with pytest.raises(WrongTypeError):
        myfunc("test", 187, val3="test2")
    with pytest.raises(WrongTypeError):
        myfunc("test", 187, val4=None)
    with pytest.raises(WrongTypeError):
        myfunc("test", 187, -1.0, None)
    with pytest.raises(WrongTypeError):
        myfunc("test", 187, -1.0, val4="test2")
    with pytest.raises(WrongTypeError):
        myfunc("test", 187, val4=None)

def test_enforce_wrapper_listtypes():
    """Ensure that fs.enforce handles lists with subtypes correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str, val2: list[int | str]):
        return int(val1)

    assert myfunc("42", []) == 42
    assert myfunc("42", [1, 2, 3]) == 42
    assert myfunc("42", ["1", "2", "3"]) == 42
    assert myfunc("42", ["test"]) == 42
    assert myfunc("42", ["test", 20]) == 42

    with pytest.raises(WrongTypeError):
        myfunc("42", ["1", "2", "3", 1.0])
    with pytest.raises(WrongTypeError):
        myfunc("42", [-0.2, "1", "2", "3"])
