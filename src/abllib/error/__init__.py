"""A module containing custom errors"""

from ._custom_exception import CustomException
from ._general import CalledMultipleTimesError, \
                      DeprecatedError, \
                      DirNotFoundError, \
                      InternalFunctionUsedError, \
                      KeyNotFoundError, \
                      LockAcquisitionTimeoutError, \
                      MissingDefaultMessageError, \
                      MissingInheritanceError, \
                      NoneTypeError, \
                      NotInitializedError, \
                      SingletonInstantiationError, \
                      WrongTypeError

__exports__ = [
    CustomException,
    CalledMultipleTimesError,
    DeprecatedError,
    DirNotFoundError,
    InternalFunctionUsedError,
    KeyNotFoundError,
    LockAcquisitionTimeoutError,
    MissingDefaultMessageError,
    MissingInheritanceError,
    NoneTypeError,
    NotInitializedError,
    SingletonInstantiationError,
    WrongTypeError
]
