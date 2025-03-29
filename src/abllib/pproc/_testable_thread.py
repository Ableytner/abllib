"""A module containing the TestableThread class"""

from threading import Thread

# original code from https://gist.github.com/sbrugman/59b3535ebcd5aa0e2598293cfa58b6ab
class TestableThread(Thread):
    """Wrapper around `threading.Thread` that propagates exceptions."""

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs=None,
                 daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.exc = None

    def run(self) -> None:
        """Invoke the callable object."""

        try:
            super().run()
        # pylint: disable-next=broad-exception-caught
        except BaseException as e:
            self.exc = e

    def join(self, timeout: float | None = None) -> None:
        """Wait until the thread terminates."""

        super().join(timeout)

        if self.exc:
            raise self.exc
