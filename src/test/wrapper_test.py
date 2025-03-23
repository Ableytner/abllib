"""Module containing tests for the abllib.wrapper module"""

# pylint: disable=function-redefined

import pytest

from abllib import error, wrapper

def test_readlock():
    """Ensure that ReadLock works as expected"""

    @wrapper.ReadLock("test1", timeout=0.1)
    def func1():
        return True

    assert not wrapper.ReadLock("test1").locked()
    assert func1()
    assert not wrapper.ReadLock("test1").locked()

    wrapper.ReadLock("test1").acquire()
    assert wrapper.ReadLock("test1").locked()
    assert wrapper.ReadLock("test1", timeout=1).locked()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        wrapper.ReadLock("test1", timeout=1).acquire()

def test_writelock():
    """Ensure that WriteLock works as expected"""

    @wrapper.WriteLock("test1", timeout=0.1)
    def func1():
        return True

    assert not wrapper.WriteLock("test1").locked()
    assert func1()
    assert not wrapper.WriteLock("test1").locked()

def test_locks_combined():
    """Ensure that ReadLock and WriteLock work together correctly"""

    @wrapper.WriteLock("test1", timeout=0.1)
    def func():
        return True

    wrapper.ReadLock("test1").acquire()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.ReadLock("test1").release()


    @wrapper.WriteLock("test2", timeout=0.1)
    def func():
        return True

    wrapper.ReadLock("test2").acquire()
    wrapper.ReadLock("test2").acquire()
    wrapper.ReadLock("test2").acquire()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.ReadLock("test2").release()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.ReadLock("test2").release()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.ReadLock("test2").release()
    func()


    @wrapper.ReadLock("test3", timeout=0.1)
    def func():
        return True

    wrapper.WriteLock("test3").acquire()
    with pytest.raises(error.LockAcquisitionTimeoutError):
        func()
    wrapper.WriteLock("test3").release()

def test_locks_underscore_names():
    """Ensure that lock names can start with an underscore"""

    lock = wrapper.ReadLock("_test1")
    assert not lock.locked()
    lock.acquire()
    assert lock.locked()
    lock.release()
    assert not lock.locked()
    assert not wrapper.ReadLock("_test1").locked()

    lock = wrapper.WriteLock("_test2")
    assert not lock.locked()
    lock.acquire()
    assert lock.locked()
    lock.release()
    assert not lock.locked()
    assert not wrapper.WriteLock("_test2").locked()

def test_single_use():
    """Ensure that singleuse cannot be initialized"""

    @wrapper.singleuse
    def func1():
        pass

    func1()

    with pytest.raises(error.CalledMultipleTimesError):
        func1()

    with pytest.raises(error.CalledMultipleTimesError):
        func1()
