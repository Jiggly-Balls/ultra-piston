from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

try:
    import httpx
except ImportError:
    pass

from .errors import MissingDataError

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Union


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

    @abstractmethod
    def get(self, endpoint: str) -> Any: ...

    @abstractmethod
    async def get_async(self, endpoint: str) -> Any: ...

    @abstractmethod
    def post(self, endpoint: str) -> Any: ...

    @abstractmethod
    async def post_async(self, endpoint: str) -> Any: ...


class HTTPXClient(AbstractHTTPClient):
    def __init__(self) -> None:
        super().__init__()
        self.driver: str = "httpx"

    def get(self, endpoint: str) -> Dict[str, Any]:
        URL: str = self._get_base_url() + endpoint
        HEADERS: Dict[str, str] = self._get_headers()

        response = httpx.get(URL, headers=HEADERS)
        return response.json()

    async def get_async(self, endpoint: str) -> str: ...

    def post(self, endpoint: str) -> None: ...

    async def post_async(self, endpoint: str) -> None: ...
