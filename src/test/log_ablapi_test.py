"""Module containing tests for the abllib.log ablapi handler"""

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from abllib import error, log
from abllib._storage import InternalStorage
from abllib.error import AblapiConnectionError, NameNotFoundError, WrongTypeError
from abllib.log._ablapi_handler import AblapiHandler, _LOG_LEVEL_MAP

def test_log_level_map():
    """Ensure that _LOG_LEVEL_MAP contains all expected mappings"""

    assert "CRITICAL" in _LOG_LEVEL_MAP
    assert _LOG_LEVEL_MAP["CRITICAL"] == "Fatal"
    assert "ERROR" in _LOG_LEVEL_MAP
    assert _LOG_LEVEL_MAP["ERROR"] == "Error"
    assert "WARNING" in _LOG_LEVEL_MAP
    assert _LOG_LEVEL_MAP["WARNING"] == "Warning"
    assert "INFO" in _LOG_LEVEL_MAP
    assert _LOG_LEVEL_MAP["INFO"] == "Information"
    assert "DEBUG" in _LOG_LEVEL_MAP
    assert _LOG_LEVEL_MAP["DEBUG"] == "Debug"
    assert "NOTSET" in _LOG_LEVEL_MAP
    assert _LOG_LEVEL_MAP["NOTSET"] == "Verbose"

def test_add_ablapi_handler_not_initialized():
    """Ensure that add_ablapi_handler raises NotInitializedError when not initialized"""

    # The clean_after_function fixture removes _log.level between tests,
    # so it should already be absent. We verify it's missing first.
    assert "_log.level" not in InternalStorage

    with pytest.raises(error.NotInitializedError):
        log.add_ablapi_handler("user-id", "token", "sender")

def test_add_ablapi_handler_invalid_args():
    """Ensure that add_ablapi_handler rejects invalid arguments"""

    log.initialize(log.LogLevel.DEBUG)

    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler(123, "token", "sender")
    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler([], "token", "sender")
    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler(None, "token", "sender")

    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler("user-id", 123, "sender")
    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler("user-id", [], "sender")

    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler("user-id", "token", sender=123)
    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler("user-id", "token", sender=[])

    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler("user-id", "token", "sender", api_url=42)
    with pytest.raises(WrongTypeError):
        log.add_ablapi_handler("user-id", "token", "sender", api_url=None)

@pytest.mark.skipif(
    not (os.environ.get("ABLAPI_USER_ID") and os.environ.get("ABLAPI_TOKEN")),
    reason="ABLAPI_USER_ID and ABLAPI_TOKEN environment variables not set",
)
def test_ablapi_handler_integration():
    """Integration test that sends a real log message to the ablapi endpoint"""

    user_id = os.environ["ABLAPI_USER_ID"]
    token = os.environ["ABLAPI_TOKEN"]

    handler = AblapiHandler(user_id, token, "abllib")
    handler.setFormatter(log._helpers._get_formatter())

    import logging

    record = logging.LogRecord(
        name="integration-test",
        level=logging.INFO,
        pathname="log_test.py",
        lineno=1,
        msg="integration test message",
        args=(),
        exc_info=None,
    )

    # This should not raise
    handler.emit(record)

    assert handler._bearer_token is not None

@pytest.mark.skipif(
    not (os.environ.get("ABLAPI_USER_ID") and os.environ.get("ABLAPI_TOKEN")),
    reason="ABLAPI_USER_ID and ABLAPI_TOKEN environment variables not set",
)
def test_add_ablapi_handler_integration():
    """Integration test for add_ablapi_handler with real API"""

    user_id = os.environ["ABLAPI_USER_ID"]
    token = os.environ["ABLAPI_TOKEN"]

    log.initialize(log.LogLevel.DEBUG)
    log.add_ablapi_handler(user_id=user_id, token=token, sender="integration-test")

    logger = log.get_logger("integration")
    logger.info("integration test via add_ablapi_handler")

    # Verify handler was registered
    assert "_log.handlers" in InternalStorage
    assert len(InternalStorage["_log.handlers"]) >= 1

    # Cleanup
    log.initialize()
