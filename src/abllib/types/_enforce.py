"""A module containing functions to enforce that given values match their type hint."""

import inspect
from time import sleep
from types import GenericAlias, UnionType
import typing
from typing import Any, Callable, Concatenate, ParamSpec, TypeVar

from .. import log
from ..error import WrongTypeError

logger = log.get_logger("types.enforce")

# dynamically inherit type hints from wrapped function
# https://github.com/python/mypy/issues/13617#issuecomment-1247745770
P = ParamSpec('P')
T = TypeVar('T')

class UnionTuple(tuple):
    """An internal class inheriting from tuple which holds all allowed types for a value"""

    def __repr__(self):
        return f"UnionTuple{super().__repr__()}"

def enforce(value_or_func: Any | Callable[P, T], target_type_or_None: Any | None = None) \
   -> None | Callable[Concatenate[str, P], T]:
    """
    Multi-purpose function for type validation.
    Can either be used directly or as a function wrapper.

    If used directly, provide the value and an annotation of the expected types.
    Alternatively use enforce_var directly.

    If used as a function wrapper, no arguments are needed.
    Alternatively use enforce_args directly.

    It the value and target_type mismatch, raise a WrongTypeError.
    """

    if inspect.isfunction(value_or_func) and target_type_or_None is None:
        return enforce_args(value_or_func)

    return enforce_var(value_or_func, target_type_or_None)

def enforce_args(func: Callable[P, T]) -> Callable[Concatenate[str, P], T]:
    """
    Wrapper function for type validation.

    If an value and annotation mismatch, raise a WrongTypeError.
    """

    arg_types: list[type] = []
    kwarg_types: dict[str, type] = {}

    sig = inspect.signature(func)
    for key, val in sig.parameters.items():
        types_annotation = _genericalias_to_types(val.annotation)

        # add args and kwargs to arg_types
        arg_types.append(types_annotation)
        logger.info(arg_types)

        if val.default != val.empty:
            # add only kwargs to kwarg_types
            kwarg_types[key] = types_annotation

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        for c, arg in enumerate(args):
            enforce_var(arg, arg_types[c])

        for key, arg in kwargs.items():
            enforce_var(arg, kwarg_types[key])

        return func(*args, **kwargs)

    return wrapper

def enforce_var(value: Any, target_type: Any) -> None:
    """
    Function for type validation.

    If the type of value and target_type mismatch, raise a WrongTypeError.
    """

    # None-types are easily handled
    if target_type is None:
        if value is None:
            # success
            return

        logger.info(f"invalid1: {value} {target_type}")
        raise WrongTypeError.with_values(value, target_type)

    # non-raising try blocks are zero-cost (the most common case here)
    # https://stackoverflow.com/a/2522013
    try:
        if isinstance(value, target_type):
            # success
            logger.info(f"valid1:   {value} {target_type}")
            return
    # TODO: use more specific exception
    # pylint: disable-next=broad-exception-caught
    except Exception:
        pass

    # start handling all special cases

    if isinstance(target_type, GenericAlias):
        # TODO: cache conversion
        target_type = _genericalias_to_types(target_type)

    if type(target_type) not in (type, list, dict, tuple, set, UnionTuple):
        logger.info(f"invalid2: {value} {target_type}")
        raise WrongTypeError(f"Expected target_type to be a valid type, not {target_type}")

    valid = _validate(value, target_type)
    if valid:
        # success
        logger.info(f"valid2:   {value} {target_type}")
        return

    logger.info(f"invalid3: {value} {target_type}")
    raise WrongTypeError.with_values(value, target_type)

def _log_io(func):
    """Log the input and output of the wrapped function"""

    c = 0
    def wrapper(*args, **kwargs):
        nonlocal c

        c += 1
        logger.info(f"({c})in:  {args} {kwargs}")

        res = func(*args, **kwargs)

        sleep(0.1)

        logger.info(f"({c})out: {res}")
        c -= 1

        sleep(0.1)

        return res
    return wrapper

@_log_io
def _genericalias_to_types(target_type: GenericAlias | Any) -> UnionTuple | list | Any:
    """
    Converts a GenericAlias
    (e.g. int|str, list[int], tuple[int, int] or dict[str, Any])
    to the internal representation
    (e.g. UnionTuple(int, str), [int], (int, int) or {str: Any})

    Any other type is returned as-is.
    """

    # any type not inheriting from GenericAlias returns None
    main_type = typing.get_origin(target_type)

    if main_type is None:
        return target_type

    if main_type == UnionType:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type.append(_genericalias_to_types(arg))

        return UnionTuple(res_type)

    if main_type == list:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type.append(_genericalias_to_types(arg))

        return res_type

    # TODO: dict, set, tuple

    logger.info(f"unhandled GenericAlias inheritent: {target_type}")
    raise RuntimeError()

# pylint: disable-next=too-many-return-statements
def _validate(value: Any, target_type: type | UnionTuple | list | dict | tuple | set) -> bool:
    """Checks if the given values' type matches the given target_type"""

    # target_type: None
    if target_type is None:
        return value is None

    # target_type: int or str or float
    if isinstance(target_type, type):
        return isinstance(value, target_type)

    # target_type: UnionTuple(int, float) or UnionTuple(str, None)
    if isinstance(target_type, UnionTuple):
        # unpack to check if any type matches
        for target in target_type:
            if _validate(value, target):
                return True
        return False

    # target_type: [] or [int] or [UnionTuple(str, float)]
    if isinstance(target_type, list):
        if not isinstance(value, list):
            return False

        # if the list has no subtypes we are done
        if len(target_type) == 0:
            return True

        # validate all list items
        for item in value:
            if not _validate(item, target_type[0]):
                return False
        return True

    # TODO: dict, set, tuple

    raise NotImplementedError(f"unhandled type: {target_type}")
