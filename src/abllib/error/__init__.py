"""A module containing custom errors"""

from abllib.error._custom_exception import CustomException
from abllib.error._general import ArgumentCombinationError as ArgumentCombinationError
from abllib.error._general import CalledMultipleTimesError as CalledMultipleTimesError
from abllib.error._general import DeprecatedError as DeprecatedError
from abllib.error._general import DirNotFoundError as DirNotFoundError
from abllib.error._general import InternalCalculationError as InternalCalculationError
from abllib.error._general import InternalFunctionUsedError as InternalFunctionUsedError
from abllib.error._general import InvalidKeyError as InvalidKeyError
from abllib.error._general import KeyNotFoundError as KeyNotFoundError
from abllib.error._general import LockAcquisitionTimeoutError as LockAcquisitionTimeoutError
from abllib.error._general import MissingDefaultMessageError as MissingDefaultMessageError
from abllib.error._general import MissingInheritanceError as MissingInheritanceError
from abllib.error._general import MissingRequiredModuleError as MissingRequiredModuleError
from abllib.error._general import NameNotFoundError as NameNotFoundError
from abllib.error._general import NoneTypeError as NoneTypeError
from abllib.error._general import NotInitializedError as NotInitializedError
from abllib.error._general import ReadonlyError as ReadonlyError
from abllib.error._general import RegisteredMultipleTimesError as RegisteredMultipleTimesError
from abllib.error._general import SingletonInstantiationError as SingletonInstantiationError
from abllib.error._general import UninitializedFieldError as UninitializedFieldError
from abllib.error._general import WrongTypeError as WrongTypeError

INTERNAL =  "Internal error, please report it on github!"

__exports__ = [
    CustomException,
    ArgumentCombinationError,
    CalledMultipleTimesError,
    DeprecatedError,
    DirNotFoundError,
    InternalCalculationError,
    InternalFunctionUsedError,
    InvalidKeyError,
    KeyNotFoundError,
    LockAcquisitionTimeoutError,
    MissingDefaultMessageError,
    MissingInheritanceError,
    MissingRequiredModuleError,
    NameNotFoundError,
    NoneTypeError,
    NotInitializedError,
    ReadonlyError,
    RegisteredMultipleTimesError,
    SingletonInstantiationError,
    UninitializedFieldError,
    WrongTypeError,
    INTERNAL
]
