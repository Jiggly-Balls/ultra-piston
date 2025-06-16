from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from typing import Optional, Union


class RequestClient(ABC):
    @final
    def __init__(
        self,
        rate_limit: Union[int, float],
        base_url: str,
        api_key: Optional[str],
    ) -> None:
        self.rate_limit: Union[int, float] = rate_limit
        self.base_url: str = base_url

    @abstractmethod
    def get(self, endpoint: str) -> str: ...

    @abstractmethod
    async def get_async(self, endpoint: str) -> str: ...
