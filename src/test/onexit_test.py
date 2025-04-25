"""Module containing tests for the abllib.onexit module"""

from abllib import error, onexit

import pytest

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
    """Ensure that registering the callbacks seperately works correctly"""

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
    """Ensure that deregistering the callbacks seperately works correctly"""

    def func1():
        pass

    onexit.register("func1", func1)

    onexit.deregister_normal_exit("func1")

    onexit.register("func1", func1)

    onexit.deregister_sigterm("func1")

    onexit.register("func1", func1)

    onexit.deregister_normal_exit("func1")
    onexit.deregister_sigterm("func1")


def test_all():
    """Ensure that all functions work together correctly"""

    def func1():
        pass

    onexit.register("func1", func1)

    onexit.deregister("func1")

    onexit.register("func1", func1)
