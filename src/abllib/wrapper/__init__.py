"""A module containing various wrappers"""

from ._deprecated import deprecated
from ._lock import Lock, Semaphore
from ._lock_wrapper import NamedLock, NamedSemaphore, ReadLock, WriteLock
from ._log_error import log_error
from ._singleuse_wrapper import singleuse

__exports__ = [
    Lock,
    NamedLock,
    NamedSemaphore,
    ReadLock,
    Semaphore,
    WriteLock,
    deprecated,
    log_error,
    singleuse
]
