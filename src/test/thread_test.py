"""Module containing tests for abllib.thread"""

# pylint: disable=missing-class-docstring

from multiprocessing import Process
from threading import Thread
from time import sleep

import pytest

from abllib.pproc import TestableThread, WorkerProcess, WorkerThread

def test_testablethread_inheritance():
    """Ensure that TestableThread inherits from Thread"""

    assert issubclass(TestableThread, Thread)

def test_testablethread_func_execution():
    """Ensure that TestableThread executes its target and then exits"""

    out = [False]
    def func1():
        out[0] = True

    t = TestableThread(target=func1)
    t.start()

    c = 0
    while c < 10 and not out[0] and t.is_alive():
        sleep(0.1)
        c += 1

    if c >= 10:
        pytest.fail("thread did not complete in time")
    assert out[0]

def test_testablethread_exception_reraise():
    """Ensure that TestableThread reraises exceptions"""

    def func1():
        raise AssertionError("This is a test message")

    t = TestableThread(target=func1)
    t.start()

    try:
        t.join()
    except AssertionError as e:
        assert str(e) == "This is a test message"
    else:
        pytest.fail("no exception raised")

def test_workerthread_inheritance():
    """Ensure that WorkerThread inherits from Thread"""

    assert issubclass(WorkerThread, Thread)

def test_workerthread_func_execution():
    """Ensure that WorkerThread executes its target and then exits"""

    out = [False]
    def func1():
        out[0] = True

    t = WorkerThread(target=func1)
    t.start()

    c = 0
    while c < 10 and not out[0] and t.is_alive():
        sleep(0.1)
        c += 1

    if c >= 10:
        pytest.fail("thread did not complete in time")
    assert out[0]

def test_workerthread_value_return():
    """Ensure that WorkerThread returns values"""

    def func1():
        return None

    t = WorkerThread(target=func1)
    t.start()

    r = t.join()
    assert r is None

    def func2():
        return ("val1", 25)

    t = WorkerThread(target=func2)
    t.start()

    r = t.join()
    assert not t.failed()
    assert r == ("val1", 25)
    assert isinstance(r[0], str)
    assert isinstance(r[1], int)

def test_workerthread_exception_return():
    """Ensure that WorkerThread returns exceptions"""

    def func1():
        raise AssertionError("This is a test message")

    t = WorkerThread(target=func1)
    t.start()

    r = t.join()
    assert t.failed()
    assert isinstance(r, BaseException)
    assert str(r) == "This is a test message"

def test_workerprocess_inheritance():
    """Ensure that WorkerProcess inherits from Process"""

    assert issubclass(WorkerProcess, Process)

def test_workerprocess_value_return():
    """Ensure that WorkerProcess returns values"""

    def func1():
        return None

    p = WorkerProcess(target=func1)
    p.start()

    r = p.join()
    assert r is None

    def func2():
        return ("val1", 25)

    p = WorkerProcess(target=func2)
    p.start()

    r = p.join()
    assert not p.failed()
    assert r == ("val1", 25)
    assert isinstance(r[0], str)
    assert isinstance(r[1], int)

def test_workerprocess_exception_return():
    """Ensure that WorkerProcess returns exceptions"""

    def func1():
        raise AssertionError("This is a test message")

    p = WorkerProcess(target=func1)
    p.start()

    r = p.join()
    assert p.failed()
    assert isinstance(r, BaseException)
    assert str(r) == "This is a test message"
