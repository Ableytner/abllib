"""Module containing tests for the abllib.wrapper module"""

# pylint: disable=protected-access, missing-class-docstring, pointless-statement, expression-not-assigned

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
