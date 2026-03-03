"""Module containing tests for the abllib.enum module"""

import enum as original_enum

from abllib import enum

# pylint: disable=missing-class-docstring

def test_create():
    """Ensure that a basic deriving Enum class works as expected"""

    class MyEnum(enum.Enum):
        TRUE = 1
        FALSE = 0

    assert issubclass(MyEnum, original_enum.Enum)
    assert issubclass(MyEnum, enum.Enum)
    assert isinstance(MyEnum.TRUE, original_enum.Enum)
    assert isinstance(MyEnum.FALSE, original_enum.Enum)

    assert MyEnum.TRUE.value == 1
    assert MyEnum.FALSE.value == 0
    assert MyEnum.TRUE.value != MyEnum.FALSE.value

def test_comparison():
    """Ensure that the new comparisons work as expected"""

    class MyEnum(enum.Enum):
        TRUE = 1
        FALSE = 0

    assert MyEnum.TRUE == 1
    assert MyEnum.FALSE == 0
    assert 1 == MyEnum.TRUE
    assert 0 == MyEnum.FALSE

    assert MyEnum.TRUE != 0
    assert MyEnum.FALSE != 1
    assert 0 != MyEnum.TRUE
    assert 1 != MyEnum.FALSE

    assert MyEnum.TRUE == MyEnum.TRUE
    assert MyEnum.FALSE == MyEnum.FALSE

    assert MyEnum.TRUE != MyEnum.FALSE
    assert MyEnum.FALSE != MyEnum.TRUE

def test_hashable():
    """Ensure that enum objects are hashable"""

    class MyEnum(enum.Enum):
        TRUE = 1
        FALSE = 0

    assert 1 in [MyEnum.TRUE]
    assert 1 not in [MyEnum.FALSE]
    assert 0 in [MyEnum.FALSE]
    assert 0 not in [MyEnum.TRUE]

    assert MyEnum.TRUE in [1]
    assert MyEnum.TRUE not in [0]
    assert MyEnum.FALSE in [0]
    assert MyEnum.FALSE not in [1]

def test_from_name():
    """Ensure that Enum.from_name works as expected"""

    class MyEnum(enum.Enum):
        TRUE = 1
        FALSE = 0

    assert MyEnum.from_name("TRUE") is MyEnum.TRUE
    assert MyEnum.from_name("FALSE") is MyEnum.FALSE

def test_from_value():
    """Ensure that Enum.from_value works as expected"""

    class MyEnum(enum.Enum):
        TRUE = 1
        FALSE = 0

    assert MyEnum.from_value(1) is MyEnum.TRUE
    assert MyEnum.from_value(0) is MyEnum.FALSE
