from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from . import __title__, __version__
from .http_clients import HTTPXClient

if TYPE_CHECKING:
    from typing import Any, Optional, Type, Union

    from .http_clients import AbstractHTTPClient


class PistonClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        rate_limit: Union[float, int] = 1.0,
        app_name: str = "Ultra-Piston-Wrapper",
        base_url: str = "https://emkc.org/api/v2/piston/",
        http_client: Type[AbstractHTTPClient] = HTTPXClient,
        **http_client_kwargs: Any,
    ) -> None:
        self._http_client: AbstractHTTPClient = http_client()

        if not self._http_client.driver:
            raise ValueError(
                f"No http `driver` was specified of {http_client=}. "
                f"Please make sure you have specified the value of the `driver` attribute in {http_client}. "
                "Example: httpx, aiohttp, requests, etc (Enter the one YOU are using)."
            )

        try:
            importlib.import_module(self._http_client.driver)
        except ModuleNotFoundError as error:
            raise ModuleNotFoundError(
                f"Couldn't find the specified HTTP driver: {self._http_client.driver} "
                f"from the passed `{http_client=}`. Please make sure you have installed "
                f"{self._http_client.driver} before running your project."
            ) from error

        if not base_url.endswith("/"):
            base_url += "/"

        self._http_client.base_url = base_url
        self._http_client.rate_limit = rate_limit
        self._http_client.headers = {
            "User-Agent": f"{self._http_client.driver}; {__title__} v{__version__}; {app_name}",
            "Content-Type": "application/json",
        }
        if api_key:
            self._http_client.headers["Authorization"] = api_key

        for key, value in http_client_kwargs.items():
            setattr(self._http_client, key, value)

    def get_runtimes(self) -> dict[str, Any]:
        return self._http_client.get("runtimes")

    async def get_runtimes_async(self) -> ...: ...

    def get_packages(self) -> ...: ...

    async def get_packages_async(self) -> ...: ...

    def post_packages(self) -> ...: ...

    async def post_packages_async(self) -> ...: ...

    def post_execute(self) -> ...: ...

    async def post_execute_async(self) -> ...: ...

    def delete_packages(self) -> ...: ...

    async def delete_packages_async(self) -> ...: ...
