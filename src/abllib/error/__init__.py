"""A module contraining custom errors"""

from .custom_exception import CustomException
from .general import DirNotFoundError, \
                     KeyNotFoundError, \
                     MissingInheritanceError, \
                     NoneTypeError, \
                     SingletonInstantiationError

__exports__ = [
    CustomException,
    DirNotFoundError,
    KeyNotFoundError,
    MissingInheritanceError,
    NoneTypeError,
    SingletonInstantiationError
]
