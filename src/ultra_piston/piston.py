from __future__ import annotations

from typing import TYPE_CHECKING

from .request_client import RequestClient

if TYPE_CHECKING:
    from typing import Optional, Type, Union


class PistonClient:
    def __init__(
        self,
        *,
        base_url: Optional[str],
        api_key: Optional[str] = None,
        rate_limit: Union[float, int] = 1.0,
        request_client: Type[RequestClient],
    ) -> None:
        self.api_key: Optional[str] = api_key
