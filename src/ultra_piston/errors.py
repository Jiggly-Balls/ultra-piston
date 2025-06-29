from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional


__all__ = (
    "BasePistonError",
    "InternalError",
    "ServerError",
    "MissingDataError",
    "BadRequestError",
    "TooManyRequestsError",
    "InternalServerError",
    "NotFoundError",
    "UnexpectedStatusError",
)


class BasePistonError(Exception):
    r"""The base exception to all ultra-piston errors."""


class InternalError(BaseException):
    r"""Errors raised internally by the wrapper."""


class ServerError(BasePistonError):
    r"""Raised for server responses that return a non-2xx (error) HTTP status code.

    Attributes
    ----------
    endpoint : Optional[str]
        | The endpoint URL.
    status_code : int
        | The status code of the server response.
    """

    def __init__(
        self, *args: Any, endpoint: Optional[str] = None, status_code: int
    ) -> None:
        super().__init__(*args)

        self.endpoint: Optional[str] = endpoint
        self.status_code: int = status_code


class MissingDataError(InternalError):
    r"""Raised when the required data is not set or is missing."""


class BadRequestError(ServerError):
    r"""Raised due to passing invalid arguments.

    Attributes
    ----------
    endpoint : Optional[str]
        | The endpoint URL.
    status_code : int
        | The status code of the server response.
    """

    def __init__(
        self, endpoint: Optional[str] = None, message: Optional[str] = None
    ) -> None:
        STATUS_CODE = 400
        message = message or (
            "Raised due to passing invalid arguments. "
            f"status_code={STATUS_CODE} | endpoint={endpoint}"
        )
        super().__init__(
            message,
            endpoint=endpoint,
            status_code=STATUS_CODE,
        )


class TooManyRequestsError(ServerError):
    r"""Raised due to sending too many requests in a short interval.

    Attributes
    ----------
    endpoint : Optional[str]
        | The endpoint URL.
    status_code : int
        | The status code of the server response.
    """

    def __init__(
        self, endpoint: Optional[str] = None, message: Optional[str] = None
    ) -> None:
        STATUS_CODE = 429
        message = message or (
            "Raised due to sending too many requests in a short interval. "
            f"status_code={STATUS_CODE} | endpoint={endpoint}"
        )
        super().__init__(
            message,
            endpoint=endpoint,
            status_code=STATUS_CODE,
        )


class InternalServerError(ServerError):
    r"""Raised due to an issue with the server.

    Attributes
    ----------
    endpoint : Optional[str]
        | The endpoint URL.
    status_code : int
        | The status code of the server response.
    """

    def __init__(
        self, endpoint: Optional[str] = None, message: Optional[str] = None
    ) -> None:
        STATUS_CODE = 500
        message = message or (
            "Raised due to an issue with the server. "
            f"status_code={STATUS_CODE} | endpoint={endpoint}"
        )

        super().__init__(
            message,
            endpoint=endpoint,
            status_code=STATUS_CODE,
        )


class NotFoundError(ServerError):
    r"""Raised when trying to access an unkown endpoint.

    Attributes
    ----------
    endpoint : Optional[str]
        | The endpoint URL.
    status_code : int
        | The status code of the server response.
    """

    def __init__(
        self, endpoint: Optional[str] = None, message: Optional[str] = None
    ) -> None:
        STATUS_CODE = 404
        message = message or (
            "Tried accessing an unkown endpoint. "
            f"status_code={STATUS_CODE} | endpoint={endpoint}"
        )

        super().__init__(
            message,
            endpoint=endpoint,
            status_code=STATUS_CODE,
        )


class UnexpectedStatusError(ServerError):
    r"""Raised for any unkown response status code (non-2xx).

    Attributes
    ----------
    endpoint : Optional[str]
        | The endpoint URL.
    status_code : int
        | The status code of the server response.
    """

    def __init__(
        self,
        status_code: int,
        endpoint: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        message = message or (
            "Unexpected response code received. "
            f"status_code={status_code} | endpoint={endpoint}"
        )

        super().__init__(
            message,
            endpoint=endpoint,
            status_code=status_code,
        )
