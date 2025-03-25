"""Module containing the ReadLock and WriteLock wrapper Classes"""

import functools
from datetime import datetime
from time import sleep
from threading import BoundedSemaphore, Lock

from .. import error
from .._storage import InternalStorage

class CustomLock():
    """
    Extends threading.Lock by allowing timeout to be None.

    threading.Lock cannot be subclassed as it is a factory function.
    https://stackoverflow.com/a/6781398
    """

    def __init__(self):
        self._lock = Lock()

    def acquire(self, blocking: bool = True, timeout: float | None = None):
        """
        Try to acquire the Lock.
        
        If blocking is disabled, it doesn't wait for the timeout.

        If timeout is set, wait for n seconds before returning.
        """

        return self._lock.acquire(blocking, -1 if timeout is None else timeout)

    def locked(self) -> bool:
        """Returns whether the Lock is held"""

        return self._lock.locked()

    def release(self):
        """Release the lock if it is currently held"""

        self._lock.release()

    def __enter__(self):
        self.acquire()

    # keep signature the same as threading.Lock
    # pylint: disable-next=redefined-builtin
    def __exit__(self, type, value, traceback):
        self.release()

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
            InternalStorage["_locks.global"] = CustomLock()

        if f"_locks.{lock_name}" not in InternalStorage:
            InternalStorage[f"_locks.{lock_name}.r"] = CustomSemaphore(999)
            InternalStorage[f"_locks.{lock_name}.w"] = CustomLock()

        self._timeout = timeout
        self._allocation_lock: CustomLock = InternalStorage["_locks.global"]

    _timeout: float | None
    _allocation_lock: CustomLock
    _lock: CustomLock | CustomSemaphore
    _other_lock: CustomLock | CustomSemaphore

    def acquire(self) -> None:
        """Acquire the lock, or throw an LockAcquisitionTimeoutError if timeout is not None"""

        if self._timeout is None:
            self._allocation_lock.acquire()

            # ensure the other lock is not held
            while self._other_lock.locked():
                sleep(0.025)

            if not self._lock.acquire():
                self._allocation_lock.release()
                raise error.LockAcquisitionTimeoutError("Internal error, please report it on github!")

            self._allocation_lock.release()
            return

        initial_time = datetime.now()
        if not self._allocation_lock.acquire(timeout=self._timeout):
            raise error.LockAcquisitionTimeoutError("Internal error, please report it on github!")

        elapsed_time = (datetime.now() - initial_time).total_seconds()

        # ensure the other lock is not held
        while self._other_lock.locked():
            sleep(0.025)
            elapsed_time += 0.025
            if elapsed_time > self._timeout:
                self._allocation_lock.release()
                raise error.LockAcquisitionTimeoutError("Internal error, please report it on github!")

        if not self._lock.acquire(timeout=self._timeout - elapsed_time):
            self._allocation_lock.release()
            raise error.LockAcquisitionTimeoutError("Internal error, please report it on github!")

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
