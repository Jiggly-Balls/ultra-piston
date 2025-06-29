from __future__ import annotations

import functools
import importlib
import logging
from typing import TYPE_CHECKING

import aiocache

from .http_clients import HTTPXClient
from .models import ExecutionOutput, File, Package, Runtime

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Type, Union

    from .http_clients import AbstractHTTPClient


__all__ = ("PistonClient",)
_logger = logging.getLogger(__name__)


class PistonClient:
    r"""
    The main client to interact with the piston-api.

    Parameters
    ----------
    api_key
        | The API key to use if any.
    rate_limit
        | Ratelimit to set for the dispatched requests.
        | Takes in a integer / float of the amount of delay between each request.
        | Defaults to 1 request per second.
    app_name
        | Name of your app / project. To be used by the HTTP client's User-Agent.
    base_url
        | Base URL of the API.
    http_client
        | The http client through which the requests are made with.
    http_client_kwargs
        | The attributes to set to the http client.
        | Useful when you want to make your own HTTP client.
    """

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

        if not driver_version:
            driver_version = "UNKOWN_VERSION"
            _logger.warning(
                "Couldn't determine driver version of library: %s.",
                driver_lib.__name__,
            )

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
        r"""Return a list of available languages."""

        runtime_data = self._http_client.get("runtimes")
        return [Runtime(**runtime) for runtime in runtime_data]

    @aiocache.cached()
    async def get_runtimes_async(self) -> List[Runtime]:
        r"""Return a list of available languages asynchronously."""

        runtime_data = await self._http_client.get_async("runtimes")
        return [Runtime(**runtime) for runtime in runtime_data]

    def get_packages(self) -> List[Package]:
        r"""Returns a list of all possible packages, and their installation status.

        .. warning::
            This method is not available for the public API.

        Raises
        ------
        :py:exc:`ultra_piston.errors.NotFoundError`
            | If the endpoint is inaccessible.
        """

        package_data = self._http_client.get("packages")
        return [Package(**package) for package in package_data]

    async def get_packages_async(self) -> List[Package]:
        r"""Returns a list of all possible packages, and their installation status asynchronously.

        .. warning::
            This method is not available for the public API.

        Raises
        ------
        :py:exc:`ultra_piston.errors.NotFoundError`
            | If the endpoint is inaccessible.
        """

        package_data = await self._http_client.get_async("packages")
        return [Package(**package) for package in package_data]

    def post_packages(self, language: str, version: str) -> None:
        r"""Install the given package.

        .. warning::
            This method is not available for the public API.

        Parameters
        ----------
        language
            | The name of the programming language.
        version
            | The version of the language.

        Raises
        ------
        :py:exc:`ultra_piston.errors.NotFoundError`
            | If the endpoint is inaccessible.

        :py:exc:`ultra_piston.errors.BadRequestError`
            | Raised if an invalid version or language was passed.
        """

        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        self._http_client.post("packages", json_data=json_data)

    async def post_packages_async(self, language: str, version: str) -> None:
        r"""Install the given package asynchronously.

        .. warning::
            This method is not available for the public API.

        Parameters
        ----------
        language
            | The name of the programming language.
        version
            | The version of the language.

        Raises
        ------
        :py:exc:`ultra_piston.errors.NotFoundError`
            | If the endpoint is inaccessible.

        :py:exc:`ultra_piston.errors.BadRequestError`
            | Raised if an invalid version or language was passed.
        """
        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        await self._http_client.post_async("packages", json_data=json_data)

    def post_execute(
        self,
        language: str,
        version: str,
        file: File,
        stdin: Optional[str] = None,
        args: Optional[List[str]] = None,
        compile_timeout: Union[float, int] = 10000,
        run_timeout: Union[float, int] = 3000,
        compile_memory_limit: int = -1,
        run_memory_limit: int = -1,
    ) -> ExecutionOutput:
        r"""Runs the given code, using the given runtime and arguments, returning the result.

        Parameters
        ----------
        language
            | The name of the programming language.
        version
            | The version of the language.
        file
            | The file containing the code to be executed.
        stdin
            | Text to pass into stdin of the program.
        args
            | Arguments to pass to the program.
        compile_timeout
            | The maximum allowed time in milliseconds for the run stage to finish before bailing out.
            | Must be a number, less than or equal to the configured maximum timeout. Defaults to maximum.
        run_timeout
            | The maximum allowed time in milliseconds for the compile stage to finish before bailing out.
            | Must be a number, less than or equal to the configured maximum timeout.
        compile_memory_limit
            | The maximum amount of memory the compile stage is allowed to use in bytes.
            | Must be a number, less than or equal to the configured maximum.
            | Defaults to maximum, or -1 (no limit) if none is configured.
        run_memory_limit
            | The maximum amount of memory the run stage is allowed to use in bytes.
            | Must be a number, less than or equal to the configured maximum.
            | Defaults to maximum, or -1 (no limit) if none is configured.

        Returns
        -------
        | Returns the ExecutionOutput data containing various data related to the ran code.

        Raises
        ------
        :py:exc:`ultra_piston.errors.BadRequestError`
            | Raised if an invalid version or language was passed.
        """

        json_data: Dict[str, Any] = {
            "language": language,
            "version": version,
            "files": [file.model_dump()],
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
        file: File,
        stdin: Optional[str] = None,
        args: Optional[List[str]] = None,
        compile_timeout: Union[float, int] = 10000,
        run_timeout: Union[float, int] = 3000,
        compile_memory_limit: int = -1,
        run_memory_limit: int = -1,
    ) -> ExecutionOutput:
        r"""Runs the given code, using the given runtime and arguments, returning the result asynchronously.

        Parameters
        ----------
        language
            | The name of the programming language.
        version
            | The version of the language.
        files
            | The file containing the code to be executed.
        stdin
            | Text to pass into stdin of the program.
        args
            | Arguments to pass to the program.
        compile_timeout
            | The maximum allowed time in milliseconds for the run stage to finish before bailing out.
            | Must be a number, less than or equal to the configured maximum timeout. Defaults to maximum.
        run_timeout
            | The maximum allowed time in milliseconds for the compile stage to finish before bailing out.
            | Must be a number, less than or equal to the configured maximum timeout.
        compile_memory_limit
            | The maximum amount of memory the compile stage is allowed to use in bytes.
            | Must be a number, less than or equal to the configured maximum.
            | Defaults to maximum, or -1 (no limit) if none is configured.
        run_memory_limit
            | The maximum amount of memory the run stage is allowed to use in bytes.
            | Must be a number, less than or equal to the configured maximum.
            | Defaults to maximum, or -1 (no limit) if none is configured.

        Returns
        -------
        Returns the ExecutionOutput data containing various data related to the ran code.

        Raises
        ------
        :py:exc:`ultra_piston.errors.BadRequestError`
            | Raised if an invalid version or language was passed.
        """

        json_data: Dict[str, Any] = {
            "language": language,
            "version": version,
            "files": [file.model_dump()],
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
        r"""Uninstall the given package.

        .. warning::
            This method is not available for the public API.

        Raises
        ------
        :py:exc:`ultra_piston.errors.NotFoundError`
            | If the endpoint is inaccessible.

        :py:exc:`ultra_piston.errors.BadRequestError`
            | Raised if an invalid version or language was passed.
        """

        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        self._http_client.delete("packages", json_data=json_data)

    async def delete_packages_async(self, language: str, version: str) -> None:
        r"""Uninstall the given package asynchronously.

        .. warning::
            This method is not available for the public API.

        Raises
        ------
        :py:exc:`ultra_piston.errors.NotFoundError`
            | If the endpoint is inaccessible.

        :py:exc:`ultra_piston.errors.BadRequestError`
            | Raised if an invalid version or language was passed.
        """

        json_data: Dict[str, str] = {
            "language": language,
            "version": version,
        }
        await self._http_client.delete_async("packages", json_data=json_data)
