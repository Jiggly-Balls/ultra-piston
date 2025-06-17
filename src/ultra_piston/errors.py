from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional


class BasePistonError(Exception):
    """The base exception to all ultra-piston errors."""


class InternalError(BaseException):
    """Errors raised internally by the wrapper."""


class ServerError(BasePistonError):
    """Raised for server responses that return a non-200 (error) HTTP status code."""

    def __init__(self, *args: Any, status_code: int) -> None:
        super().__init__(*args)

        self.status_code = status_code


class MissingDataError(InternalError):
    """Raised when the required data is not set or is missing."""


class TooManyRequests(ServerError):
    """Raised due to sending too many requests in a short interval."""

    def __init__(self, message: Optional[str] = None) -> None:
        status_code = 429
        super().__init__(
            message
            or f"Raised due to sending too many requests in a short interval. status_code={status_code}.",
            status_code=status_code,
        )


class InternalServerError(ServerError):
    """Raised due to an issue with the server."""

    def __init__(self, message: Optional[str] = None) -> None:
        status_code = 500
        super().__init__(
            message
            or f"Raised due to an issue with the server. status_code={status_code}.",
            status_code=status_code,
        )


class UnexpectedStatusError(ServerError):
    """Raised for any unkown response status code (non-2xx)."""

    def __init__(
        self, status_code: int, message: Optional[str] = None
    ) -> None:
        super().__init__(
            message
            or f"Unexpected response code received. status_code={status_code}.",
            status_code=status_code,
        )
