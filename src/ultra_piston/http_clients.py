from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

try:
    import httpx
except ImportError:
    pass

from .errors import (
    InternalServerError,
    MissingDataError,
    NotFoundError,
    TooManyRequests,
    UnexpectedStatusError,
)

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Union

    from httpx import Response


class AbstractHTTPClient(ABC):
    def __init__(self) -> None:
        self.driver: Optional[str] = None
        self.rate_limit: Optional[Union[int, float]] = None
        self.base_url: Optional[str] = None
        self.headers: Optional[Dict[str, str]] = None

    def _get_rate_limit(self) -> Union[int, float]:
        if not self.rate_limit:
            raise MissingDataError(
                f"Missing valid value for the attribute `self.rate_limit` of {self.__class__}."
            )
        return self.rate_limit

    def _get_base_url(self) -> str:
        if not self.base_url:
            raise MissingDataError(
                f"Missing valid value for the attribute `self.base_url` of {self.__class__}."
            )
        return self.base_url

    def _get_headers(self) -> Dict[str, str]:
        if not self.headers:
            raise MissingDataError(
                f"Missing valid value for the attribute `self.headers` of {self.__class__}."
            )
        return self.headers

    def _get_http_payload(self, endpoint: str = "") -> Dict[str, Any]:
        BASE_URL = self._get_base_url() + endpoint
        HEADERS = self._get_headers()

        return {"url": BASE_URL, "headers": HEADERS}

    @abstractmethod
    def get(self, endpoint: str) -> Any: ...

    @abstractmethod
    async def get_async(self, endpoint: str) -> Any: ...

    @abstractmethod
    def post(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any: ...

    @abstractmethod
    async def post_async(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any: ...


class HTTPXClient(AbstractHTTPClient):
    def __init__(self) -> None:
        super().__init__()
        self.driver: str = "httpx"

    def _validate_response_status(self, response: Response) -> Any:
        if 300 > response.status_code > 199:
            return response.json()

        elif response.status_code == 404:
            raise NotFoundError(str(response.url))

        elif response.status_code == 429:
            raise TooManyRequests(str(response.url))

        elif response.status_code == 500:
            raise InternalServerError(str(response.url))

        else:
            raise UnexpectedStatusError(
                response.status_code, str(response.url)
            )

    def get(self, endpoint: str) -> Any:
        payload = self._get_http_payload(endpoint)

        response = httpx.get(**payload)
        return self._validate_response_status(response=response)

    async def get_async(self, endpoint: str) -> Any:
        payload = self._get_http_payload(endpoint)

        async with httpx.AsyncClient() as client:
            response = await client.get(**payload)

        return self._validate_response_status(response=response)

    def post(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any:
        payload = self._get_http_payload(endpoint)
        if json_data:
            payload["json"] = json_data

        response = httpx.post(**payload)
        return self._validate_response_status(response=response)

    async def post_async(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any:
        payload = self._get_http_payload(endpoint)
        if json_data:
            payload["json"] = json_data

        async with httpx.AsyncClient() as client:
            response = await client.post(**payload)

        return self._validate_response_status(response=response)
