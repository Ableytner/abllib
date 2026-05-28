"""A module containing various wrappers"""

from abllib.wrapper._deprecated import deprecated as deprecated
from abllib.wrapper._lock import Lock as Lock
from abllib.wrapper._lock import Semaphore as Semaphore
from abllib.wrapper._lock_wrapper import NamedLock as NamedLock
from abllib.wrapper._lock_wrapper import NamedSemaphore as NamedSemaphore
from abllib.wrapper._lock_wrapper import ReadLock as ReadLock
from abllib.wrapper._lock_wrapper import WriteLock as WriteLock
from abllib.wrapper._log_error import log_error as log_error
from abllib.wrapper._log_io import log_io as log_io
from abllib.wrapper._singleuse_wrapper import singleuse as singleuse
from abllib.wrapper._timeit import timeit as timeit

__exports__ = [
    Lock,
    NamedLock,
    NamedSemaphore,
    ReadLock,
    Semaphore,
    WriteLock,
    deprecated,
    log_error,
    log_io,
    timeit,
    singleuse
]
