"""Module containing tests for the abllib.wrapper module"""

import pytest

from abllib import error, wrapper

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
