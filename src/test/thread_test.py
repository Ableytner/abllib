"""Module containing tests for abllib.thread"""

# pylint: disable=missing-class-docstring

from threading import Thread
from time import sleep

import pytest

from abllib.thread import TestableThread

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
