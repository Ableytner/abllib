"""Module containing custom exceptions for general usage"""

# pylint: disable=arguments-differ

from typing import Any

from ._custom_exception import CustomException

class CalledMultipleTimesError(CustomException):
    """Exception raised when a single-use function is called twice"""

    default_messages = {
        0: "The function can only be called once"
    }

class DeprecatedError(CustomException):
    """Exception raised when deprecated functionality is used"""

    default_messages = {
        0: "This functionality is deprecated",
        1: "This functionality is deprecated, please use {0} instead"
    }

class DirNotFoundError(CustomException):
    """Exception raised when an expected directory doesn't exist"""

    default_messages = {
        0: "The expected directory doesn't exist",
        1: "The expected directory '{0}' doesn't exist"
    }

class InternalFunctionUsedError(CustomException):
    """Exception raised when an internal function was used by an external project"""

    default_messages = {
        0: "This function is only for library-internal use"
    }

class KeyNotFoundError(CustomException):
    """Exception raised when the key is not found in the storage"""

    default_messages = {
        0: "The requested key could not be found",
        1: "The requested key '{0}' could not be found"
    }

class LockAcquisitionTimeoutError(CustomException):
    """Exception raised when the acquisitgion of a lock timed out"""

    default_messages = {
        0: "The requested lock could not be acquired in time"
    }

class MissingDefaultMessageError(CustomException):
    """Exception raised when an error class is missing the default message"""

    default_messages = {
        0: "The error class is missing a default message. Set it as a class variable in default_messages[0].",
        1: "The error class '{0}' is missing a default message. Set it as a class variable in default_messages[0]."
    }

class MissingInheritanceError(CustomException):
    """Exception raised when a class is expected to inherit from another class"""

    default_messages = {
        0: "The class is missing an inheritance from another class",
        1: "The class is missing an inheritance from '{0}'",
        2: "The class '{0}' is missing an inheritance from '{1}'"
    }

class NoneTypeError(CustomException):
    """Exception raised when a value is unexpectedly None"""

    default_messages = {
        0: "Didn't expect None as a value here"
    }

class NotInitializedError(CustomException):
    """Exception raised when an instance is used before it is correctly initialized"""

    default_messages = {
        0: "The instance is not yet initialized correctly"
    }

class SingletonInstantiationError(CustomException):
    """Exception raised when a singleton class is instantiated twice"""

    default_messages = {
        0: "The singleton class can only be instantiated once",
        1: "The singleton class '{0}' can only be instantiated once"
    }

class WrongTypeError(CustomException):
    """Exception raised when a value wasn't of an expected type"""

    default_messages = {
        0: "Received an unexpected type",
        2: "Expected {1}, not {0}"
    }

    @classmethod
    def with_values(cls, received: Any | type, expected: Any | type):
        if not isinstance(received, type):
            received = type(received)
        if not isinstance(expected, type):
            expected = type(expected)

        return super().with_values(received, expected)
