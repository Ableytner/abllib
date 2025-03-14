"""A module containing the ThreadWithReturnValue class"""

from threading import Thread
from typing import Any

# original code from https://stackoverflow.com/a/6894023
class ThreadWithReturnValue(Thread):
    """A parent class of threading.Thread which returns a value on join()"""

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=None,
                 kwargs=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            try:
                self._return = self._target(*self._args, **self._kwargs)
            # pylint: disable-next=broad-exception-caught
            except Exception as e:
                self._return = e

    def join(self, *args) -> Any | Exception:
        Thread.join(self, *args)
        return self._return
