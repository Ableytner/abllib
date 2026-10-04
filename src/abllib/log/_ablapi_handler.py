"""A module containing the ablapi log handler"""

from __future__ import annotations

import base64
import json
import logging
import urllib.error
import urllib.request

from abllib import error
from abllib._storage import InternalStorage
from abllib.error._general import AblapiConnectionError
from abllib.log._helpers import _setup_handler

# Mapping from Python logging level names to Serilog log level strings
_LOG_LEVEL_MAP: dict[str, str] = {
    "CRITICAL": "Fatal",
    "ERROR": "Error",
    "WARNING": "Warning",
    "INFO": "Information",
    "DEBUG": "Debug",
    "NOTSET": "Verbose",
}

class AblapiHandler(logging.Handler):
    """
    A logging handler that sends log messages to the ablapi LogController endpoint.
    Authenticates using Basic auth (userId:token) to obtain a JWT, then uses
    that JWT as a Bearer token for all subsequent log requests.
    """

    def __init__(self, user_id: str, token: str, sender: str, api_url: str = "https://api.ableytner.at") -> None:
        super().__init__()
        self._user_id = user_id
        self._token = token
        self._sender = sender
        self._api_url = api_url.rstrip("/")
        self._bearer_token: str | None = None

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record to the ablapi endpoint.

        Authenticates on first emit if not already authenticated.
        """

        if self._bearer_token is None:
            self._authenticate()

        log_level = _LOG_LEVEL_MAP.get(record.levelname, "Information")
        message = self.format(record)
        self._send_log(log_level, message)

    def _authenticate(self) -> None:
        credentials = base64.b64encode(
            f"{self._user_id}:{self._token}".encode("utf-8")
        ).decode("utf-8")

        url = f"{self._api_url}/auth"
        request = urllib.request.Request(
            url,
            data=b"",
            method="POST",
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status != 200:
                    raise AblapiConnectionError(
                        f"Authentication failed with status {response.status}"
                    )
                body = json.loads(response.read().decode("utf-8"))
                self._bearer_token = body.get("token")
                if not self._bearer_token:
                    raise AblapiConnectionError("Received invalid response: missing token")
        except urllib.error.HTTPError as exc:
            if exc.code == 401:
                raise AblapiConnectionError("Invalid Userid / Token") from exc
            raise AblapiConnectionError(
                f"Authentication request failed with status {exc.code}"
            ) from exc
        except urllib.error.URLError as exc:
            raise AblapiConnectionError(
                f"Failed to connect to API at {self._api_url}: {exc.reason}"
            ) from exc

    def _send_log(self, log_level: str, message: str) -> None:
        url = f"{self._api_url}/log"
        payload = json.dumps({
            "log_level": log_level,
            "sender": self._sender,
            "message": message,
        }).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {self._bearer_token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status == 401:
                    # Token may have expired; retry authentication once
                    self._authenticate()
                    request.headers["Authorization"] = f"Bearer {self._bearer_token}"
                    with urllib.request.urlopen(request, timeout=10) as retry_response:
                        if retry_response.status != 200:
                            raise AblapiConnectionError(
                                f"Log request failed with status {retry_response.status}"
                            )
                elif response.status != 200:
                    raise AblapiConnectionError(
                        f"Log request failed with status {response.status}"
                    )
        except urllib.error.HTTPError as exc:
            if exc.code == 401:
                self._authenticate()
                request.headers["Authorization"] = f"Bearer {self._bearer_token}"
                try:
                    with urllib.request.urlopen(request, timeout=10) as retry_response:
                        if retry_response.status != 200:
                            raise AblapiConnectionError(
                                f"Log request failed with status {retry_response.status}"
                            ) from exc
                except urllib.error.HTTPError as retry_exc:
                    raise AblapiConnectionError(
                        f"Log request failed with status {retry_exc.code}"
                    ) from retry_exc
            else:
                raise AblapiConnectionError(
                    f"Log request failed with status {exc.code}"
                ) from exc
        except urllib.error.URLError as exc:
            raise AblapiConnectionError(
                f"Failed to connect to API at {self._api_url}: {exc.reason}"
            ) from exc

def add_ablapi_handler(user_id: str, token: str, sender: str, api_url: str = "https://api.ableytner.at") -> None:
    """
    Add an ablapi handler to the root logger.

    Log messages will be sent to the ablapi LogController endpoint
    using the provided UserId and Token for authentication.
    """

    if "_log.level" not in InternalStorage:
        raise error.NotInitializedError("log.initialize() needs to be called first")

    if not isinstance(user_id, str):
        raise error.WrongTypeError.with_values(user_id, str)
    if not isinstance(token, str):
        raise error.WrongTypeError.with_values(token, str)
    if not isinstance(api_url, str):
        raise error.WrongTypeError.with_values(api_url, str)
    if not isinstance(sender, str):
        raise error.WrongTypeError.with_values(sender, str)

    handler = AblapiHandler(
        user_id,
        token,
        sender,
        api_url,
    )

    _setup_handler(handler)
