from __future__ import annotations

import asyncio
import functools
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict

try:
    import httpx
except ModuleNotFoundError:
    pass

from .errors import (
    InternalServerError,
    MissingDataError,
    NotFoundError,
    TooManyRequests,
    UnexpectedStatusError,
)

if TYPE_CHECKING:
    from asyncio import Queue
    from typing import (
        Any,
        Awaitable,
        Callable,
        Dict,
        Optional,
        ParamSpec,
        TypeVar,
        Union,
    )

    from httpx import Response

    P = ParamSpec("P")
    R = TypeVar("R")


__all__ = ("AbstractHTTPClient", "HTTPXClient")


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

    @abstractmethod
    def delete(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any: ...

    @abstractmethod
    async def delete_async(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any: ...


class HTTPXClient(AbstractHTTPClient):
    def __init__(self) -> None:
        super().__init__()

        self.driver: str = "httpx"
        self._last_request: Optional[datetime] = None
        self._request_queue: Queue[Awaitable[Any]] = asyncio.Queue(maxsize=1)

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

    @staticmethod
    def sync_ratelimit(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            instance: HTTPXClient = args[0]  # type: ignore -- VSC editor bug in showing reportAssignmentType error.

            if instance._last_request:
                now = datetime.now()
                future_request_time = instance._last_request + timedelta(
                    seconds=instance._get_rate_limit()
                )
                if now < future_request_time:
                    cool_down = (future_request_time - now).seconds
                    time.sleep(cool_down)

            result = func(*args, **kwargs)

            instance._last_request = datetime.now()

            return result

        return wrapper

    @staticmethod
    def async_ratelimit(
        func: Callable[P, Awaitable[R]],
    ) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            event_loop = asyncio.get_event_loop()
            instance: HTTPXClient = args[0]  # type: ignore

            if instance._last_request is not None:
                now = datetime.now()
                valid_future_stamp = instance._last_request + timedelta(
                    seconds=instance._get_rate_limit()
                )
                if now < valid_future_stamp:
                    # Rate limited
                    cool_down = (valid_future_stamp - now).seconds
                    await asyncio.sleep(cool_down)

            instance._last_request = datetime.now()

            future_await = func(*args, **kwargs)
            task_fetch = event_loop.create_task(
                instance._create_queue(future_await)
            )
            task_data = await asyncio.wait([task_fetch])
            return task_data[0].pop().result()

        return wrapper

    async def _create_queue(self, coro: Awaitable[R]) -> R:
        await self._request_queue.put(coro)
        awaitable = await self._request_queue.get()
        return await awaitable

    @sync_ratelimit
    def get(self, endpoint: str) -> Any:
        payload = self._get_http_payload(endpoint)
        response = httpx.get(**payload)
        return self._validate_response_status(response=response)

    @async_ratelimit
    async def get_async(self, endpoint: str) -> Any:  # pyright:ignore[reportIncompatibleMethodOverride]
        payload = self._get_http_payload(endpoint)

        async with httpx.AsyncClient() as client:
            response = await client.get(**payload)

        return self._validate_response_status(response=response)

    @sync_ratelimit
    def post(
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any:
        payload = self._get_http_payload(endpoint)
        if json_data:
            payload["json"] = json_data

        response = httpx.post(**payload)
        return self._validate_response_status(response=response)

    @async_ratelimit
    async def post_async(  # pyright:ignore[reportIncompatibleMethodOverride]
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any:
        payload = self._get_http_payload(endpoint)
        if json_data:
            payload["json"] = json_data

        async with httpx.AsyncClient() as client:
            response = await client.post(**payload)

        return self._validate_response_status(response=response)

    @sync_ratelimit
    def delete(
        self, endpoint: str, json_data: Dict[Any, Any] | None = None
    ) -> Any:
        payload = self._get_http_payload(endpoint)
        payload["method"] = "DELETE"
        if json_data:
            payload["json"] = json_data

        response = httpx.request(**payload)
        return self._validate_response_status(response=response)

    @async_ratelimit
    async def delete_async(  # pyright:ignore[reportIncompatibleMethodOverride]
        self, endpoint: str, json_data: Optional[Dict[Any, Any]] = None
    ) -> Any:
        payload = self._get_http_payload(endpoint)
        if json_data:
            payload["json"] = json_data

        async with httpx.AsyncClient() as client:
            response = await client.request(**payload)

        return self._validate_response_status(response=response)
