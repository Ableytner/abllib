"""A module containing custom errors"""

from ._custom_exception import CustomException
from ._general import CalledMultipleTimesError, \
                      DeprecatedError, \
                      DirNotFoundError, \
                      InternalCalculationError, \
                      InternalFunctionUsedError, \
                      KeyNotFoundError, \
                      LockAcquisitionTimeoutError, \
                      MissingDefaultMessageError, \
                      MissingInheritanceError, \
                      NameNotFoundError, \
                      NoneTypeError, \
                      NotInitializedError, \
                      RegisteredMultipleTimesError, \
                      SingletonInstantiationError, \
                      WrongTypeError

INTERNAL =  "Internal error, please report it on github!"

__exports__ = [
    CustomException,
    CalledMultipleTimesError,
    DeprecatedError,
    DirNotFoundError,
    InternalCalculationError,
    InternalFunctionUsedError,
    KeyNotFoundError,
    LockAcquisitionTimeoutError,
    MissingDefaultMessageError,
    MissingInheritanceError,
    NameNotFoundError,
    NoneTypeError,
    NotInitializedError,
    RegisteredMultipleTimesError,
    SingletonInstantiationError,
    WrongTypeError,
    INTERNAL
]
