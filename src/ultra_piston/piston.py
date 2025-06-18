from __future__ import annotations

import functools
import importlib
from typing import TYPE_CHECKING

from .http_clients import HTTPXClient
from .models import ExecutionOutput, File, Package, Runtime

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Type, Union

    from .http_clients import AbstractHTTPClient


__all__ = ("PistonClient",)


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
        driver_version: Optional[str] = None

        if not self._http_client.driver:
            raise ValueError(
                f"No http `driver` was specified of `http_client={http_client}`. "
                f"Please make sure you have specified the value of the `driver` attribute in `{http_client}`. "
                "Example: httpx, aiohttp, requests, etc."
            )

        try:
            driver_lib = importlib.import_module(self._http_client.driver)

        except ModuleNotFoundError as error:
            raise ModuleNotFoundError(
                f"Couldn't find the specified HTTP driver: `{self._http_client.driver}` "
                f"from the passed `http_client={http_client}`. Please make sure you have installed "
                f"`{self._http_client.driver}` before running your project."
            ) from error

        driver_version = getattr(driver_lib, "__version__")
        if not driver_version:
            version_info = getattr(driver_lib, "version_info")
            if version_info:
                try:
                    driver_version = ".".join(version_info)
                except:  # noqa: E722
                    pass
        driver_version = driver_version or "UNKOWN_VERSION"

        if not base_url.endswith("/"):
            base_url += "/"

        self._http_client.base_url = base_url
        self._http_client.rate_limit = rate_limit
        self._http_client.headers = {
            "User-Agent": f"{self._http_client.driver} {driver_version}; {app_name}",
            "Content-Type": "application/json",
        }
        if api_key:
            self._http_client.headers["Authorization"] = api_key

        for key, value in http_client_kwargs.items():
            setattr(self._http_client, key, value)

    @functools.cache
    def get_runtimes(self) -> List[Runtime]:
        runtime_data = self._http_client.get("runtimes")
        return [Runtime(**runtime) for runtime in runtime_data]

    @functools.cache
    async def get_runtimes_async(self) -> List[Runtime]:
        runtime_data = await self._http_client.get_async("runtimes")
        return [Runtime(**runtime) for runtime in runtime_data]

    def get_packages(self) -> List[Package]:
        package_data = self._http_client.get("packages")
        return [Package(**package) for package in package_data]

    async def get_packages_async(self) -> List[Package]:
        package_data = await self._http_client.get_async("packages")
        return [Package(**package) for package in package_data]

    def post_packages(self, language: str, version: str) -> None:
        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        self._http_client.post("packages", json_data=json_data)

    async def post_packages_async(self, language: str, version: str) -> None:
        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        await self._http_client.post_async("packages", json_data=json_data)

    def post_execute(
        self,
        language: str,
        version: str,
        files: List[File],
        stdin: Optional[str] = None,
        args: Optional[List[str]] = None,
        compile_timeout: Union[float, int] = 10000,
        run_timeout: Union[float, int] = 3000,
        compile_memory_limit: int = -1,
        run_memory_limit: int = -1,
    ) -> ExecutionOutput:
        json_data: Dict[str, Any] = {
            "language": language,
            "version": version,
            "files": [file.model_dump() for file in files],
            "compile_timeout": compile_timeout,
            "run_timeout": run_timeout,
            "compile_memory_limit": compile_memory_limit,
            "run_memory_limit": run_memory_limit,
        }
        if stdin:
            json_data["stdin"] = stdin
        if args:
            json_data["args"] = args

        response = self._http_client.post("execute", json_data=json_data)
        return ExecutionOutput(**response)

    async def post_execute_async(
        self,
        language: str,
        version: str,
        files: List[File],
        stdin: Optional[str] = None,
        args: Optional[List[str]] = None,
        compile_timeout: Union[float, int] = 10000,
        run_timeout: Union[float, int] = 3000,
        compile_memory_limit: int = -1,
        run_memory_limit: int = -1,
    ) -> ExecutionOutput:
        json_data: Dict[str, Any] = {
            "language": language,
            "version": version,
            "files": [file.model_dump() for file in files],
            "compile_timeout": compile_timeout,
            "run_timeout": run_timeout,
            "compile_memory_limit": compile_memory_limit,
            "run_memory_limit": run_memory_limit,
        }
        if stdin:
            json_data["stdin"] = stdin
        if args:
            json_data["args"] = args

        response = await self._http_client.post_async(
            "execute", json_data=json_data
        )
        return ExecutionOutput(**response)

    def delete_packages(self, language: str, version: str) -> None:
        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        self._http_client.delete("packages", json_data=json_data)

    async def delete_packages_async(self, language: str, version: str) -> None:
        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        await self._http_client.delete_async("packages", json_data=json_data)
