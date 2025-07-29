"""Module containing tests for the abllib.wrapper module"""

# pylint: disable=function-redefined, consider-using-with, unused-argument

import re
import os
from datetime import datetime

import pytest

from abllib import error, wrapper, log
from abllib.pproc import WorkerThread

def test_lock():
    """Ensure that Lock works as expected"""

    assert hasattr(wrapper, "Lock")
    assert callable(wrapper.Lock)

    lock = wrapper.Lock()

    assert not lock.locked()
    assert lock.acquire(blocking=True, timeout=1)
    assert lock.locked()

    assert not lock.acquire(blocking=True, timeout=1)

    lock.release()
    assert not lock.locked()

def test_semaphore():
    """Ensure that Semaphore works as expected"""

    assert hasattr(wrapper, "Semaphore")
    assert callable(wrapper.Semaphore)

    sem = wrapper.Semaphore(3)

    assert not sem.locked()
    assert sem.acquire(blocking=True, timeout=1)
    assert sem.locked()
    assert sem.acquire(blocking=True, timeout=1)
    assert sem.locked()
    assert sem.acquire(blocking=True, timeout=1)
    assert sem.locked()

    # the semaphore is full
    assert not sem.acquire(blocking=True, timeout=1)

    sem.release()
    assert sem.locked()
    sem.release()
    assert sem.locked()
    sem.release()
    assert not sem.locked()

def test_namedlock():
    """Ensure that NamedLock works as expected"""

    assert hasattr(wrapper, "NamedLock")
    assert callable(wrapper.NamedLock)

    @wrapper.NamedLock("test1", timeout=0.1)
    def func1():
        return True

    assert not wrapper.NamedLock("test1").locked()
    assert func1()
    assert not wrapper.NamedLock("test1").locked()

    wrapper.NamedLock("test2").acquire()
    assert wrapper.NamedLock("test2").locked()
    assert wrapper.NamedLock("test2", timeout=1).locked()

    wrapper.NamedLock("test3").acquire()
    def func2():
        assert wrapper.NamedLock("test3").locked()
        wrapper.NamedLock("test3", timeout=4).acquire()

    start_time = datetime.now()
    thread = WorkerThread(target=func2)
    thread.start()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        thread.join(reraise=True)

    duration = datetime.now() - start_time
    assert duration.total_seconds() > 3.5
    assert duration.total_seconds() < 4.5

def test_namedsemaphore():
    """Ensure that NamedSemaphore works as expected"""

    assert hasattr(wrapper, "NamedSemaphore")
    assert callable(wrapper.NamedSemaphore)

    @wrapper.NamedSemaphore("test1", timeout=0.1)
    def func1():
        return True

    assert not wrapper.NamedSemaphore("test1").locked()
    assert func1()
    assert not wrapper.NamedSemaphore("test1").locked()

    wrapper.NamedSemaphore("test2").acquire()
    assert wrapper.NamedSemaphore("test2").locked()
    assert wrapper.NamedSemaphore("test2", timeout=1).locked()

    wrapper.NamedLock("test3").acquire()
    def func2():
        assert not wrapper.NamedSemaphore("test3").locked()
        wrapper.NamedSemaphore("test3", timeout=4).acquire()

    start_time = datetime.now()
    thread = WorkerThread(target=func2)
    thread.start()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        thread.join(reraise=True)

    duration = datetime.now() - start_time
    assert duration.total_seconds() > 3.5
    assert duration.total_seconds() < 4.5

def test_namedlocks_combined():
    """Ensure that NamedLock and NamedSemaphore work together correctly"""

    @wrapper.NamedLock("test1", timeout=0.1)
    def func():
        return True

    wrapper.NamedSemaphore("test1").acquire()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.NamedSemaphore("test1").release()


    @wrapper.NamedLock("test2", timeout=0.1)
    def func():
        return True

    wrapper.NamedSemaphore("test2").acquire()
    wrapper.NamedSemaphore("test2").acquire()
    wrapper.NamedSemaphore("test2").acquire()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.NamedSemaphore("test2").release()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.NamedSemaphore("test2").release()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.NamedSemaphore("test2").release()
    func()


    @wrapper.NamedSemaphore("test3", timeout=0.1)
    def func():
        return True

    wrapper.NamedLock("test3").acquire()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.NamedLock("test3").release()

def test_locks_underscore_names():
    """Ensure that named lock names can start with an underscore"""

    lock = wrapper.NamedSemaphore("_test1")
    assert not lock.locked()
    lock.acquire()
    assert lock.locked()
    assert wrapper.NamedSemaphore("_test1").locked()
    lock.release()
    assert not lock.locked()
    assert not wrapper.NamedSemaphore("_test1").locked()

    lock = wrapper.NamedLock("_test2")
    assert not lock.locked()
    lock.acquire()
    assert lock.locked()
    assert wrapper.NamedLock("_test2").locked()
    lock.release()
    assert not lock.locked()
    assert not wrapper.NamedLock("_test2").locked()

def test_singleuse():
    """Ensure that singleuse works as expected"""

    @wrapper.singleuse
    def func1():
        pass

    func1()

    with pytest.raises(error.CalledMultipleTimesError):
        func1()

    with pytest.raises(error.CalledMultipleTimesError):
        func1()

def test_singleuse_exception():
    """Ensure that raised exceptions reset singleuse flag"""

    data = [1, 2, 3]

    @wrapper.singleuse
    def func1():
        if len(data) > 0:
            data.pop(0)
            raise error.InternalCalculationError()

    with pytest.raises(error.InternalCalculationError):
        func1()
    with pytest.raises(error.InternalCalculationError):
        func1()
    with pytest.raises(error.InternalCalculationError):
        func1()

    func1()

    with pytest.raises(error.CalledMultipleTimesError):
        func1()

    with pytest.raises(error.CalledMultipleTimesError):
        func1()

def test_log_error_default(capture_logs):
    """Ensure that log_error uses the root logger by default"""

    @wrapper.log_error
    def func1():
        raise RuntimeError("my message")

    with pytest.raises(RuntimeError):
        func1()

    assert os.path.isfile("test.log")
    with open("test.log", "r", encoding="utf8") as f:
        content = f.readlines()

        # remove "pointer" lines only present in python 3.12
        content = list(filter(lambda x: x.strip().strip("^") != "", content))

        assert len(content) == 7
        assert re.match(r"\[.*\] \[ERROR   \] root: my message", content[0])
        assert re.match(r"Traceback \(most recent call last\):", content[1])
        assert re.match(r"  File \".*_log_error.py\", line \d+, in wrapper", content[2])
        assert re.match(r"    return func\(\*args, \*\*kwargs\)", content[3])
        assert re.match(r"  File \".*wrapper_test.py\", line \d+, in func1", content[4])
        assert re.match(r"    raise RuntimeError\(\"my message\"\)", content[5])
        assert re.match(r"RuntimeError: my message", content[6])

def test_log_error_loggername(capture_logs):
    """Ensure that log_error uses the provided logger name"""

    @wrapper.log_error("mycustomlogger")
    def func1():
        raise RuntimeError("my message")

    with pytest.raises(RuntimeError):
        func1()

    assert os.path.isfile("test.log")
    with open("test.log", "r", encoding="utf8") as f:
        content = f.readlines()

        # remove "pointer" lines only present in python 3.12
        content = list(filter(lambda x: x.strip().strip("^") != "", content))

        assert len(content) == 7
        assert re.match(r"\[.*\] \[ERROR   \] mycustomlogger: my message", content[0])
        assert re.match(r"Traceback \(most recent call last\):", content[1])
        assert re.match(r"  File \".*_log_error.py\", line \d+, in wrapper", content[2])
        assert re.match(r"    return func\(\*args, \*\*kwargs\)", content[3])
        assert re.match(r"  File \".*wrapper_test.py\", line \d+, in func1", content[4])
        assert re.match(r"    raise RuntimeError\(\"my message\"\)", content[5])
        assert re.match(r"RuntimeError: my message", content[6])

def test_log_error_customlogger(capture_logs):
    """Ensure that log_error uses the provided custom logger"""

    @wrapper.log_error(log.get_logger("mycustomlogger"))
    def func1():
        raise RuntimeError("my message")

    with pytest.raises(RuntimeError):
        func1()

    assert os.path.isfile("test.log")
    with open("test.log", "r", encoding="utf8") as f:
        content = f.readlines()

        # remove "pointer" lines only present in python 3.12
        content = list(filter(lambda x: x.strip().strip("^") != "", content))

        assert len(content) == 7
        assert re.match(r"\[.*\] \[ERROR   \] mycustomlogger: my message", content[0])
        assert re.match(r"Traceback \(most recent call last\):", content[1])
        assert re.match(r"  File \".*_log_error.py\", line \d+, in wrapper", content[2])
        assert re.match(r"    return func\(\*args, \*\*kwargs\)", content[3])
        assert re.match(r"  File \".*wrapper_test.py\", line \d+, in func1", content[4])
        assert re.match(r"    raise RuntimeError\(\"my message\"\)", content[5])
        assert re.match(r"RuntimeError: my message", content[6])

def test_log_error_handler():
    """Ensure that log_error uses the provided handler"""

    results = []
    def myhandler(exc_text):
        results.append(exc_text)

    @wrapper.log_error(handler=myhandler)
    def func1():
        raise RuntimeError("my message")

    with pytest.raises(RuntimeError):
        func1()

    assert len(results) == 1
    assert results[0] == "RuntimeError: my message"
