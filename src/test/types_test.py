"""Module containing tests for the abllib.types module"""

# pylint: disable=missing-class-docstring, unused-argument, missing-function-docstring

from typing import Literal

import pytest

from abllib import types
from abllib.error import WrongTypeError, WrongValueError

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

def test_enforce_wrapper_uniontypes():
    """Ensure that fs.enforce handles UnionTypes correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str | None, val2: int | float):
        return str(val2)

    assert myfunc("test", 187) == "187"
    assert myfunc("test", 187.1) == "187.1"
    assert myfunc(None, 187) == "187"
    assert myfunc(None, 187.1) == "187.1"

    with pytest.raises(WrongTypeError):
        myfunc("test", "187")
    with pytest.raises(WrongTypeError):
        myfunc(1.5, 187)
    with pytest.raises(WrongTypeError):
        myfunc(None, None)
    with pytest.raises(WrongTypeError):
        myfunc(187, 187)

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

def test_enforce_wrapper_dicttypes():
    """Ensure that fs.enforce handles dicts with subtypes correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str, val2: dict[int, str | None]):
        return int(val1)

    assert myfunc("42", {}) == 42
    assert myfunc("42", {1: "test", 2: "test2"}) == 42
    assert myfunc("42", {1: None, 2: None}) == 42
    assert myfunc("42", {1: None, 2: "test"}) == 42
    assert myfunc("42", {1: "test", 2: None}) == 42
    assert myfunc("42", {1: "test", 2: "test2", 3: "test3", 4: "test4", 5: None, 6: "test6"}) == 42

    with pytest.raises(WrongTypeError):
        myfunc("42", {1.1: None})
    with pytest.raises(WrongTypeError):
        myfunc("42", {None: "test"})
    with pytest.raises(WrongTypeError):
        myfunc("42", {1: "test", 2: "test2", 3: "test3", 4: "test4", 5: 5.1})

def test_enforce_wrapper_tupletypes():
    """Ensure that fs.enforce handles tuples with subtypes correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str, val2: tuple[int | str, str, str | None]):
        return int(val1)

    assert myfunc("42", (1, "2", "3")) == 42
    assert myfunc("42", ("1", "2", "3")) == 42
    assert myfunc("42", ("test", "test2", None)) == 42
    assert myfunc("42", (20, "test", None)) == 42

    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", 2, "3"))
    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", "2", 3))
    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", 2, 3))
    with pytest.raises(WrongTypeError):
        myfunc("42", (0.1, "2", "3"))
    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", (2, 2), "3"))

def test_enforce_wrapper_tupletypes_ellipsis():
    """Ensure that fs.enforce handles tuples with an Ellipsis subtype correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str, val2: tuple[int, ...]):
        return int(val1)

    assert myfunc("42", ()) == 42
    assert myfunc("42", (1)) == 42
    assert myfunc("42", (1, 2, 3)) == 42

    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", 2, "3"))
    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", "2", 3))
    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", 2, 3))
    with pytest.raises(WrongTypeError):
        myfunc("42", (0.1, "2", "3"))
    with pytest.raises(WrongTypeError):
        myfunc("42", ("1", (2, 2), "3"))

def test_enforce_wrapper_settypes():
    """Ensure that fs.enforce handles sets with subtypes correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(val1: str, val2: set[int | float]):
        return int(val1)

    assert myfunc("42", set()) == 42
    assert myfunc("42", set([1, 2])) == 42
    assert myfunc("42", set([2.5])) == 42
    assert myfunc("42", set([1.01, -2.02, 3, 4, 5.05])) == 42
    assert myfunc("42", set([1, 1, 1])) == 42

    with pytest.raises(WrongTypeError):
        myfunc("42", set([1, "2", 3, 1.0]))
    with pytest.raises(WrongTypeError):
        myfunc("42", set([-0.2, 1, 2, "3"]))
    with pytest.raises(WrongTypeError):
        myfunc("42", set([-0.2, "test"]))

def test_enforce_wrapper_class_members():
    """Ensure that fs.enforce handles class member functions correctly"""

    assert callable(types.enforce)

    class MyClass:
        @types.enforce
        def myfunc(self, val1: str, val2: int | None):
            return int(val1)

    m = MyClass()

    assert m.myfunc("42", 0) == 42
    assert m.myfunc("42", None) == 42
    assert m.myfunc("3", 9999999) == 3

    with pytest.raises(WrongTypeError):
        m.myfunc("42", 0.1)
    with pytest.raises(WrongTypeError):
        m.myfunc(42, 1)
    with pytest.raises(WrongTypeError):
        m.myfunc(None, 15)

def test_enforce_literal():
    """Ensure that fs.enforce handles literal values correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(myarg: Literal["ok", "cancelled"]):
        return 42

    assert myfunc("ok") == 42
    assert myfunc("cancelled") == 42
    with pytest.raises(WrongValueError):
        myfunc("notok")
    with pytest.raises(WrongValueError):
        myfunc("")
    with pytest.raises(WrongValueError):
        myfunc(10)
    with pytest.raises(WrongValueError):
        myfunc(None)

def test_enforce_mixed():
    """Ensure that fs.enforce handles types and literal values mixed correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(myarg: Literal["ok", "cancelled"] | bool | None):
        return 42

    assert myfunc("ok") == 42
    assert myfunc("cancelled") == 42
    assert myfunc(True) == 42
    assert myfunc(False) == 42
    assert myfunc(None) == 42
    with pytest.raises(WrongTypeError):
        myfunc("notok")
    with pytest.raises(WrongTypeError):
        myfunc(10)
    with pytest.raises(WrongTypeError):
        myfunc(5.7)

def test_enforce_return():
    """Ensure that fs.enforce handles return values correctly"""

    assert callable(types.enforce)

    @types.enforce
    def myfunc(myarg) -> int | float:
        return myarg

    assert myfunc(42) == 42
    assert myfunc(-10000) == -10000
    assert myfunc(1.5) == 1.5
    with pytest.raises(WrongTypeError):
        myfunc("test")
    with pytest.raises(WrongTypeError):
        myfunc(None)
