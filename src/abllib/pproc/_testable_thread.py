"""A module containing the TestableThread class"""

from typing import Any

from ._worker_thread import WorkerThread

# original code from https://gist.github.com/sbrugman/59b3535ebcd5aa0e2598293cfa58b6ab
class TestableThread(WorkerThread):
    """Wrapper around `abllib.pproc.WorkerThread` that propagates exceptions on join."""

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs=None,
                 daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

    def join(self, timeout: float | None = None) -> Any:
        """Wait until the thread terminates and raise any caught exceptions."""

        ret_value_or_error = super().join(timeout)

        if isinstance(ret_value_or_error, BaseException):
            raise ret_value_or_error

        return ret_value_or_error
