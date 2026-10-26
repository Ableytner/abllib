"""Module containing tests for the abllib.onexit module"""

import re
import signal
import subprocess
import sys

import pytest

from abllib import error, fs, onexit
from abllib.pproc import WorkerThread

# pylint: disable=protected-access, unused-argument

def test_register():
    """Ensure that registering the same callback multiple times raises an error"""

    def func1():
        pass

    onexit.register("func1", func1)

    with pytest.raises(error.RegisteredMultipleTimesError):
        onexit.register("func1", func1)

    with pytest.raises(error.RegisteredMultipleTimesError):
        onexit.register("func1", func1)

def test_deregister():
    """Ensure that deregistering the same callback multiple times raises an error"""

    def func1():
        pass

    onexit.register("func1", func1)

    onexit.deregister("func1")

    with pytest.raises(error.NameNotFoundError):
        onexit.deregister("func1")

    with pytest.raises(error.NameNotFoundError):
        onexit.deregister("func1")

def test_register_single():
    """Ensure that registering the callbacks separately works correctly"""

    def func1():
        pass

    onexit.register_normal_exit("func1", func1)

    onexit.deregister("func1")

    onexit.register_sigterm("func1", func1)

    onexit.deregister("func1")

    onexit.register_normal_exit("func1", func1)
    onexit.register_sigterm("func1", func1)

    onexit.deregister("func1")

def test_deregister_single():
    """Ensure that deregistering the callbacks separately works correctly"""

    def func1():
        pass

    onexit.register("func1", func1)

    onexit.deregister_normal_exit("func1")

    onexit.register("func1", func1)

    onexit.deregister_sigterm("func1")

    onexit.register("func1", func1)

    onexit.deregister_normal_exit("func1")
    onexit.deregister_sigterm("func1")

def test_register_all():
    """Ensure that all register functions work together correctly"""

    def func1():
        pass

    onexit.register("func1", func1)

    onexit.deregister("func1")

    onexit.register("func1", func1)

def test_call_atexit():
    """Ensure that atexit function calls callbacks correctly"""

    data = [False]
    def func1():
        data[0] = True

    onexit.register("func1", func1)

    onexit._atexit_func()

    assert data[0]

def test_call_signal():
    """Ensure that signal function calls callbacks correctly"""

    data = [False]
    def func1():
        data[0] = True

    onexit.register("func1", func1)

    onexit._signal_func(None, None)

    assert data[0]

def test_ctrl_c():
    """Ensure that the callback runs exactly once when the process is interrupted by CTRL+C (SIGINT)"""

    src_dir = fs.absolute(__file__, "..", "..")

    script = f"""
import os
import signal
import sys
import threading
import time

sys.path.insert(0, {src_dir!r})

from abllib import onexit

def cleanup():
    print("CLEANUP_RAN", flush=True)

onexit.register("ctrl_c", cleanup)

def send_sigint():
    time.sleep(0.5)
    # send KeyboardInterrupt
    os.kill(os.getpid(), signal.SIGINT)

threading.Thread(target=send_sigint, daemon=True).start()
time.sleep(10)
print("SURVIVED", flush=True)
"""

    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=15, check=False)

    assert result.returncode == -signal.SIGINT
    assert result.stdout.count("CLEANUP_RAN") == 1
    assert "SURVIVED" not in result.stdout

def test_dotname():
    """Ensure that names containing a "." work as expected"""

    data = [False]
    def func1():
        data[0] = True

    onexit.register("func1.cb", func1)

    onexit._atexit_func()

    assert data[0]

def test_register_otherthread(capture_logs):
    """Ensure that registering from another thread logs a warning"""

    def func1():
        pass

    t = WorkerThread(target=lambda: onexit.register("func1", func1))
    t.start()

    res = t.join()

    assert res is None

    with open("test.log", "r", encoding="utf8") as f:
        content = f.readlines()
        assert len(content) == 1
        assert re.match(r"\[.*\] \[WARNING \] onexit: Tried to use onexit module from non-main thread", content[0])

    # function should not have be registered
    onexit.register("func1", func1)
    with pytest.raises(error.RegisteredMultipleTimesError):
        onexit.register("func1", func1)
