"""Module containing the NamedLock and NamedSemaphore classes"""

from __future__ import annotations

import functools
from datetime import datetime
from time import sleep

from ._lock import Lock, Semaphore
from .. import error
from .._storage import InternalStorage

class _BaseNamedLock():
    """
    The base class for the ReadLock and WriteLock classes.
    """

    def __init__(self, lock_name: str, timeout: int | float | None = None):
        if isinstance(timeout, int):
            timeout = float(timeout)

        # TODO: add type validation
        if not isinstance(lock_name, str):
            raise error.WrongTypeError.with_values(lock_name, str)
        if not isinstance(timeout, float) and timeout is not None:
            raise error.WrongTypeError.with_values(timeout, float, None)

        self._name = lock_name
        self._timeout = timeout

        if "_locks" not in InternalStorage:
            InternalStorage["_locks.global"] = Lock()
        self._allocation_lock: Lock = InternalStorage["_locks.global"]

    _name: str
    _lock: Lock | Semaphore
    _timeout: float | None
    _allocation_lock: Lock

    @property
    def name(self) -> str:
        return self._name

    def acquire(self) -> None:
        """Acquire the lock, or throw an LockAcquisitionTimeoutError if timeout is not None"""

        if self._timeout is None:
            self._allocation_lock.acquire()

            # ensure the other lock is not held
            other = self._get_other()
            if other is not None:
                while other.locked():
                    sleep(0.025)

            if not self._lock.acquire():
                self._allocation_lock.release()
                raise error.LockAcquisitionTimeoutError()

            self._allocation_lock.release()
            return

        initial_time = datetime.now()
        if not self._allocation_lock.acquire(timeout=self._timeout):
            raise error.LockAcquisitionTimeoutError(error.INTERNAL)

        elapsed_time = (datetime.now() - initial_time).total_seconds()

        # ensure the other lock is not held
        other = self._get_other()
        if other is not None:
            while other.locked():
                sleep(0.025)
                elapsed_time += 0.025
                if elapsed_time > self._timeout:
                    self._allocation_lock.release()
                    raise error.LockAcquisitionTimeoutError()

        if not self._lock.acquire(timeout=self._timeout - elapsed_time):
            self._allocation_lock.release()
            raise error.LockAcquisitionTimeoutError()

        self._allocation_lock.release()

    def release(self) -> None:
        """Release the lock"""

        self._lock.release()

    def locked(self) -> bool:
        """Return whether the lock is currentyl held"""

        return self._lock.locked()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __call__(self, func):
        """Called when instance is used as a decorator"""

        def wrapper(*args, **kwargs):
            """The wrapped function that is called on function execution"""

            with self:
                ret = func(*args, **kwargs)

            return ret

        # https://stackoverflow.com/a/17705456/15436169
        functools.update_wrapper(wrapper, func)

        return wrapper

    def _get_other(self) -> _BaseNamedLock | None:
        raise NotImplementedError()

class NamedLock(_BaseNamedLock):
    """
    Make a function require a lock to be held during execution.

    Only a single WriteLock can hold the lock, but only if the ReadLock is not currently held.

    Optionally provide a timeout in seconds,
    after which an LockAcquisitionTimeoutError is thrown (disabled if timeout is None).
    """

    def __init__(self, lock_name, timeout = None):
        super().__init__(lock_name, timeout)

        if f"_locks.{lock_name}.l" not in InternalStorage:
            InternalStorage[f"_locks.{lock_name}.l"] = Lock()

        self._lock = InternalStorage[f"_locks.{lock_name}.l"]

    def _get_other(self):
        if f"_locks.{self.name}.s" in InternalStorage:
            return InternalStorage[f"_locks.{self.name}.s"]
        return None

class NamedSemaphore(_BaseNamedLock):
    """
    Make a function require a lock to be held during execution.

    Multiple ReadLocks can hold the same lock concurrently, but only if the WriteLock is not currently held.

    Optionally provide a timeout in seconds,
    after which an LockAcquisitionTimeoutError is thrown (disabled if timeout is None).
    """

    def __init__(self, lock_name, timeout = None):
        super().__init__(lock_name, timeout)

        if f"_locks.{lock_name}.s" not in InternalStorage:
            InternalStorage[f"_locks.{lock_name}.s"] = Semaphore(999)

        self._lock = InternalStorage[f"_locks.{lock_name}.s"]

    def _get_other(self):
        if f"_locks.{self.name}.l" in InternalStorage:
            return InternalStorage[f"_locks.{self.name}.l"]
        return None

# deprecated
ReadLock = NamedSemaphore

# deprecated
WriteLock = NamedLock
