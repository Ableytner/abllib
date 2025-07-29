"""A module containing functions to enforce that given values match their type hint."""

import inspect
import typing
from types import GenericAlias, UnionType
from typing import (Any, Callable, Concatenate, Literal, ParamSpec, TypeVar,
                    Union)

from .. import log
from ..error import InvalidTypeHintError, WrongTypeError, WrongValueError

logger = log.get_logger("types.enforce")

# dynamically inherit type hints from wrapped function
# https://github.com/python/mypy/issues/13617#issuecomment-1247745770
P = ParamSpec('P')
T = TypeVar('T')

class UnionTuple(tuple):
    """An internal class inheriting from tuple which holds all allowed types for a value"""

    def __repr__(self):
        return f"UnionTuple{super().__repr__()}"

class LiteralTuple(tuple):
    """An internal class inheriting from tuple which holds all allowed values for a value"""

    def __repr__(self):
        return f"LiteralTuple{super().__repr__()}"

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

    If the return value and annotation mismatch, also raise a WrongTypeError.
    """

    arg_types: list[type] = []
    kwarg_types: dict[str, type] = {}

    sig = inspect.signature(func)
    for key, val in sig.parameters.items():
        # ignore undecorated arguments
        # pylint: disable-next=protected-access
        if val.annotation is inspect._empty:
            types_annotation = Any
        elif isinstance(val.annotation, str):
            # if 'from __future__ import annotations' is present, all type hints are literal strings
            # e.g. "str" or "int | None", not <class 'str'> or <class 'types.UnionType'>
            try:
                # pylint: disable-next=eval-used
                types_annotation = _genericalias_to_types(eval(val.annotation))
            except NameError:
                logger.warning(f"recursive type hints are not yet supported, ignoring instead: {val.annotation}")
                types_annotation = Any
        else:
            types_annotation = _genericalias_to_types(val.annotation)

        # add args and kwargs to arg_types
        arg_types.append(types_annotation)

        if val.default != val.empty:
            # add only kwargs to kwarg_types
            kwarg_types[key] = types_annotation

    # ignore undecorated return
    # pylint: disable-next=protected-access
    if sig.return_annotation is inspect._empty:
        return_type = Any
    elif isinstance(sig.return_annotation, str):
        # if 'from __future__ import annotations' is present, all type hints are literal strings
        # e.g. "str" or "int | None", not <class 'str'> or <class 'types.UnionType'>
        try:
            # pylint: disable-next=eval-used
            return_type = _genericalias_to_types(eval(sig.return_annotation))
        except NameError:
            logger.warning(f"recursive type hints are not yet supported, ignoring instead: {sig.return_annotation}")
            return_type = Any
    else:
        return_type = _genericalias_to_types(sig.return_annotation)

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        for c, arg in enumerate(args):
            enforce_var(arg, arg_types[c])

        for key, arg in kwargs.items():
            enforce_var(arg, kwarg_types[key])

        ret = func(*args, **kwargs)

        enforce_var(ret, return_type)

        return ret

    return wrapper

def enforce_var(value: Any, target_type: Any) -> None:
    """
    Function for type validation.

    If the type of value and target_type mismatch, raise a WrongTypeError.
    """

    # Any means the value was not decorated at all
    if target_type is Any:
        # success
        return

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
    # if the target_type is a GenericAlias / custom types class
    except TypeError:
        pass

    # start handling all special cases

    if isinstance(target_type, GenericAlias):
        target_type = _genericalias_to_types(target_type)

    if type(target_type) not in (type, list, dict, tuple, set, UnionTuple, LiteralTuple):
        raise WrongTypeError(f"Expected target_type to be a valid type, not '{target_type}'")

    valid = _validate(value, target_type)
    if valid:
        # success
        return

    if isinstance(target_type, LiteralTuple):
        raise WrongValueError.with_values(value, *target_type[:5])

    raise WrongTypeError.with_values(value, target_type)

# pylint: disable-next=too-many-return-statements
def _genericalias_to_types(target_type: GenericAlias | Any) \
   -> UnionTuple | list | dict | tuple | set | LiteralTuple | Any:
    """
    Converts a GenericAlias
    (e.g. int|str or list[int] or tuple[int, int] or dict[str, Any])
    to the internal representation
    (e.g. UnionTuple(int, str) or [int] or (int, int) or {str: Any})

    Any other type is returned as-is.
    """

    # any type not inheriting from GenericAlias returns None
    main_type = typing.get_origin(target_type)

    if main_type is None:
        return target_type

    if main_type in [UnionType, Union]:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type.append(_genericalias_to_types(arg))

        return UnionTuple(res_type)

    if main_type == list:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type.append(_genericalias_to_types(arg))

        return res_type

    if main_type == dict:
        args = typing.get_args(target_type)
        if len(args) != 2:
            raise InvalidTypeHintError(f"'dict' type hint expected 2 args, not {len(args)}")

        res_type = {
            _genericalias_to_types(args[0]): _genericalias_to_types(args[1])
        }

        return res_type

    if main_type == tuple:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type.append(_genericalias_to_types(arg))

        return tuple(res_type)

    if main_type == set:
        res_type = []

        for arg in typing.get_args(target_type):
            res_type.append(_genericalias_to_types(arg))

        return set(res_type)

    # pylint: disable-next=comparison-with-callable
    if main_type == Literal:
        return LiteralTuple(typing.get_args(target_type))

    raise RuntimeError(f"unhandled GenericAlias inheritent: {target_type}")

# pylint: disable-next=too-many-return-statements
def _validate(value: Any, target_type: type | UnionTuple | LiteralTuple | list | dict | tuple | set) -> bool:
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

    # target_type: LiteralTuple("ok", "cancel") or LiteralTuple(0, 2, 3)
    if isinstance(target_type, LiteralTuple):
        # unpack to check if any value matches
        for target in target_type:
            if value == target:
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

    # target_type: {} or {str: str} or {int: UnionTuple(str, float, None)}
    if isinstance(target_type, dict):
        if not isinstance(value, dict):
            return False

        # if the dict has no subtypes we are done
        if len(target_type) == 0:
            return True

        # validate all dict items
        key_type, item_type = list(target_type.items())[0]
        for key, item in value.items():
            if not _validate(key, key_type):
                return False
            if not _validate(item, item_type):
                return False
        return True

    # target_type: () or (int, int) or (UnionTuple(str, float), float) or (str, ...)
    if isinstance(target_type, tuple):
        if not isinstance(value, tuple):
            return False

        # if the tuple has no subtypes we are done
        if len(target_type) == 0:
            return True

        # tuple should be variable length with homogenous types
        if len(target_type) == 2 and target_type[1] == Ellipsis:
            for item in value:
                if not _validate(item, target_type[0]):
                    return False
            return True

        # value is either too long or too short
        if len(target_type) != len(value):
            return False

        # validate all tuple items
        for c, item_type in enumerate(target_type):
            # zero-cost try block
            try:
                if not _validate(value[c], item_type):
                    return False
            except IndexError:
                return False

        return True

    # target_type: set() or set(int) or set(UnionTuple(str, float))
    if isinstance(target_type, set):
        if not isinstance(value, set):
            return False

        # if the set has no subtypes we are done
        if len(target_type) == 0:
            return True

        # validate all set items
        for item in value:
            if not _validate(item, list(target_type)[0]):
                return False
        return True

    raise NotImplementedError(f"unhandled type: {target_type}")
