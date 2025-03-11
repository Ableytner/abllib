"""A module contraining custom errors"""

from .custom_exception import CustomException
from .general import CalledMultipleTimesError, \
                     DirNotFoundError, \
                     KeyNotFoundError, \
                     MissingInheritanceError, \
                     NoneTypeError, \
                     SingletonInstantiationError

__exports__ = [
    CustomException,
    CalledMultipleTimesError,
    DirNotFoundError,
    KeyNotFoundError,
    MissingInheritanceError,
    NoneTypeError,
    SingletonInstantiationError
]
