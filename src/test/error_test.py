"""Module containing tests for the different types of errors"""

# pylint: disable=missing-class-docstring

import pytest

from abllib import error

def test_customexception_inheritance():
    """Ensure that CustomException inherits from Exception"""

    assert issubclass(error.CustomException, Exception)

def test_customexception_custom_message():
    """Ensure that CustomException instantiation with a custom messaage keeps the message"""

    class TestException(error.CustomException):
        default_message = "This exception is used in tests"

    try:
        raise TestException("This message should be retained")
    except TestException as e:
        assert str(e) == "This message should be retained"
    else:
        pytest.fail("Expected an exception")

def test_customexception_default_message():
    """Ensure that CustomException instantiation without a custom messaage uses the default message"""

    class TestException(error.CustomException):
        default_message = "This exception is used in tests"

    try:
        raise TestException()
    except TestException as e:
        assert str(e) == "This exception is used in tests"
    else:
        pytest.fail("Expected an exception")

def test_wrongtypeerror():
    """Ensure that WrongTypeError handles optional args correctly"""

    try:
        raise error.WrongTypeError()
    except error.WrongTypeError as e:
        assert str(e) == "Received an unexpected type"
    else:
        pytest.fail("Expected an exception")

    try:
        raise error.WrongTypeError("This is a custom error message")
    except error.WrongTypeError as e:
        assert str(e) == "This is a custom error message"
    else:
        pytest.fail("Expected an exception")

    try:
        raise error.WrongTypeError(("20", int))
    except error.WrongTypeError as e:
        assert str(e) == "Expected <class 'int'>, received <class 'str'>"
    else:
        pytest.fail("Expected an exception")
