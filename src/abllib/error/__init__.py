"""A module contraining custom errors"""

from .custom_exception import CustomException
from .general import CalledMultipleTimesError, \
                     DirNotFoundError, \
                     KeyNotFoundError, \
                     MissingInheritanceError, \
                     NoneTypeError, \
                     SingletonInstantiationError
from .wrong_type_error import WrongTypeError

__exports__ = [
    CustomException,
    CalledMultipleTimesError,
    DirNotFoundError,
    KeyNotFoundError,
    MissingInheritanceError,
    NoneTypeError,
    SingletonInstantiationError,
    WrongTypeError
]
