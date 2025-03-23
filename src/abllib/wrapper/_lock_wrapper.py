"""Module containing the ReadLock and WriteLock wrapper Classes"""

import functools
from datetime import datetime
from time import sleep
from threading import BoundedSemaphore, Lock

from .. import error
from .._storage import InternalStorage

# we can't use the default threading.Semaphore
# because we need a semaphore with value == 0 if it isn't held
# This is the opposite behaviour of threading.Semaphore
class CustomSemaphore(BoundedSemaphore):
    """
    Extends threading.BoundedSemaphore by adding a locked() function.

    This makes it equivalent to threading.Lock usage-wise.
    """

    def locked(self) -> bool:
        """Returns whether the Semaphore is held at least once"""

        return self._value != self._initial_value

class _BaseLock():
    """
    The base class for the ReadLock and WriteLock classes.
    """

    def __init__(self, lock_name: str, timeout: int | float | None = None):
        if isinstance(timeout, int):
            timeout = float(timeout)

        # TODO: add type validation
        if not isinstance(lock_name, str):
            raise error.WrongTypeError((lock_name, str))
        if not isinstance(timeout, float) and timeout is not None:
            raise error.WrongTypeError((timeout, (float, None)))

        if "_locks" not in InternalStorage:
            InternalStorage["_locks.global"] = Lock()

        if f"_locks.{lock_name}" not in InternalStorage:
            InternalStorage[f"_locks.{lock_name}.r"] = CustomSemaphore(999)
            InternalStorage[f"_locks.{lock_name}.w"] = Lock()

        self._timeout = timeout
        self._allocation_lock: Lock = InternalStorage["_locks.global"]

    _timeout: float | None
    _allocation_lock: type[Lock]
    _lock: CustomSemaphore | type[Lock]
    _other_lock: CustomSemaphore | type[Lock]

    def acquire(self) -> None:
        """Acquire the lock, optionally throwing an LockAcquisitionTimeoutError"""

        if self._timeout is None:
            self._allocation_lock.acquire()

            # ensure the other lock is not held
            while self._other_lock.locked():
                sleep(0.025)
        else:
            initial_time = datetime.now()
            if not self._allocation_lock.acquire(timeout=self._timeout):
                raise error.LockAcquisitionTimeoutError("Internal error, please report it on github!")

            elapsed_time = (datetime.now() - initial_time).total_seconds() * 1000

            # ensure the writelock is not held
            while self._other_lock.locked() > 0:
                sleep(0.025)
                elapsed_time += 0.025
                if elapsed_time > self._timeout:
                    self._allocation_lock.release()
                    raise error.LockAcquisitionTimeoutError("Internal error, please report it on github!")

        try:
            self._lock.acquire(timeout=self._timeout)
        finally:
            self._allocation_lock.release()

    def __enter__(self):
        self.acquire()

    def release(self) -> None:
        """Release the lock"""

        self._lock.release()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def locked(self) -> bool:
        """Return whether the lock is currentyl held"""

        return self._lock.locked()

    def __call__(self, func):
        """Called when instance is used as a decorator"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """The wrapped function that is called on function execution"""

            with self:
                ret = func(*args, **kwargs)

            return ret

        return wrapper

class ReadLock(_BaseLock):
    """
    Make a function require a lock to be held during execution.

    Multiple ReadLocks can hold the same lock concurrently, but only if the WriteLock is not currently held.

    Optionally provide a timeout in seconds,
    after which an LockAcquisitionTimeoutError is thrown (disabled if timeout is None).
    """

    def __init__(self, lock_name, timeout = None):
        super().__init__(lock_name, timeout)

        self._lock = InternalStorage[f"_locks.{lock_name}.r"]
        self._other_lock = InternalStorage[f"_locks.{lock_name}.w"]

class WriteLock(_BaseLock):
    """
    Make a function require a lock to be held during execution.

    Only a single WriteLock can hold the lock, but only if the ReadLock is not currently held.

    Optionally provide a timeout in seconds,
    after which an LockAcquisitionTimeoutError is thrown (disabled if timeout is None).
    """

    def __init__(self, lock_name, timeout = None):
        super().__init__(lock_name, timeout)

        self._lock = InternalStorage[f"_locks.{lock_name}.w"]
        self._other_lock = InternalStorage[f"_locks.{lock_name}.r"]
