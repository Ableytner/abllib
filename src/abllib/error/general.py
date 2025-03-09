"""Module containing custom exceptions for general usage"""

from .custom_exception import CustomException

class DirNotFoundError(CustomException):
    """Exception raised when an expected directory doesn't exist"""

    default_message = "The expected directory doesn't exist"

class KeyNotFoundError(CustomException):
    """Exception raised when the key is not found in the storage"""

    default_message = "The requested key could not be found"

class MissingInheritanceError(CustomException):
    """Exception raised when a class is expected to inherit from another class"""

    default_message = "The class is missing an inheritance from another class"

class NoneTypeError(CustomException):
    """Exception raised when a value is unexpectedly None"""

    default_message = "DIdn't expect None as a value here"

class SingletonInstantiationError(CustomException):
    """Exception raised when a singleton class is instantiated twice"""

    default_message = "The singleton class can only be instantiated once"
