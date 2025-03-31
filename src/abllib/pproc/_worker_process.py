"""A module containing the WorkerProcess class"""

# pylint: disable=dangerous-default-value

from multiprocessing import Process, Queue
from typing import Any

import dill

class WorkerProcess(Process):
    """Wrapper around `multiprocessing.Process` that stores and returns resulting values and exceptions."""

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs={},
                 daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        # use dill instead of pickle
        # https://stackoverflow.com/a/72776044/15436169
        self._target = dill.dumps(self._target)
        self._return_queue = Queue(maxsize=1)
        self._failed_queue = Queue(maxsize=1)

    def run(self) -> None:
        """Invoke the callable object."""

        if self._target is not None:
            try:
                target = dill.loads(self._target)
                return_value = target(*self._args, **self._kwargs)
                self._return_queue.put(return_value)
            # pylint: disable-next=broad-exception-caught
            except BaseException as e:
                self._return_queue.put(e)
                self._failed_queue.put(None)

        else:
            self._return_queue.put(None)

    def join(self, timeout: float | None = None, reraise: bool = False) -> Any | BaseException:
        """Wait until the child process terminates."""

        super().join(timeout)

        return_value = self._return_queue.get(block=False)

        # put return_value back to allow multiple .join() calls
        self._return_queue.put(return_value)

        if reraise and isinstance(return_value, BaseException):
            raise return_value

        return return_value

    def failed(self) -> bool:
        """Return whether target execution raised an exception."""

        return not self._failed_queue.empty()
