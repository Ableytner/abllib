"""A module contraining custom errors"""

from ._custom_exception import CustomException
from ._general import CalledMultipleTimesError, \
                     DirNotFoundError, \
                     KeyNotFoundError, \
                     MissingInheritanceError, \
                     NoneTypeError, \
                     SingletonInstantiationError
from ._wrong_type_error import WrongTypeError

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
