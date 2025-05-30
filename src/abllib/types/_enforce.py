"""A module containing functions to enforce that given values match their type hint."""

import inspect
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

def enforce(value_or_func: Any | Callable[P, T], target_type_or_None: Any = None) \
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

        # also add all kwargs to arg_types
        arg_types.append(types_annotation)

        if val.default != val.empty:
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

    If value and target_type mismatch, raise a WrongTypeError.
    """

    # None-types are easily handled
    if target_type is None:
        if value is None:
            # success
            return

        raise WrongTypeError.with_values(value, target_type)

    # non-raising try blocks are zero-cost (the most common case here)
    # https://stackoverflow.com/a/2522013
    try:
        if isinstance(value, target_type):
            # success
            return
    # pylint: disable-next=broad-exception-caught
    except Exception:
        pass

    # start handling all special cases

    if isinstance(target_type, GenericAlias):
        # TODO: cache conversion
        target_type = _genericalias_to_types(target_type)

    if type(target_type) not in (list, dict, tuple, set, type):
        raise WrongTypeError(f"Expected target_type to be a valid type, not {target_type}")

    valid = _validate(value, target_type)
    if valid:
        return

    logger.info(f"invalid: {value} {target_type}")
    raise WrongTypeError.with_values(value, target_type)

def _genericalias_to_types(target_type: GenericAlias) -> tuple[Any]:
    if isinstance(target_type, type):
        return (target_type,)

    main_type = typing.get_origin(target_type)

    if main_type == list:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type += _genericalias_to_types(arg)

        return res_type
    # TODO: dict, set, tuple

    if main_type == UnionType:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type += _genericalias_to_types(arg)

        return tuple(res_type)

    logger.info(f"unhandled type: {target_type}")
    raise RuntimeError()

def _validate(value: Any, *target_types: list | dict | tuple | set | type) -> bool:
    validated = False

    for target_type in target_types:
        # target_type is None:
        if target_type is None and value is None:
            return True

        # target_type is int or str or float
        if isinstance(target_type, type) and isinstance(value, target_type):
            return True

        # target_type is [] or [int] or [str, float]
        if isinstance(target_type, list) and isinstance(value, list):
            # if the list has no subtypes we are done
            if len(target_type) == 0:
                return True

            # validate all list items
            items_valid = True
            for item in value:
                if not _validate(item, *target_type):
                    items_valid = False
                    break
            if items_valid:
                return True

    return validated
