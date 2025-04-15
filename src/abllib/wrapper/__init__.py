"""A module containing various wrappers"""

from ._lock import Lock, Semaphore
from ._lock_wrapper import NamedLock, NamedSemaphore
from ._singleuse_wrapper import singleuse

__exports__ = [
    Lock,
    Semaphore,
    NamedLock,
    NamedSemaphore,
    singleuse
]
