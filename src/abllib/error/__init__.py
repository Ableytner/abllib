"""A module contraining custom errors"""

from .custom_exception import CustomException
from .general import DirNotFoundError, \
                     KeyNotFoundError, \
                     MissingInheritanceError, \
                     NoneTypeError, \
                     SingletonInstantiationError
from .wrong_type_error import WrongTypeError

__exports__ = [
    CustomException,
    DirNotFoundError,
    KeyNotFoundError,
    MissingInheritanceError,
    NoneTypeError,
    SingletonInstantiationError,
    WrongTypeError
]
