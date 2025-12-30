import abc
from typing import Dict, Optional

class DispatchProvider(abc.ABC):
    @abc.abstractmethod
    async def get_dispatch_mw_by_tech(self, zone: Optional[str] = None) -> Dict[str, float]:
        ...

    @abc.abstractmethod
    async def get_price_eur_mwh(self, zone: Optional[str] = None) -> float:
        ...

    @abc.abstractmethod
    async def health_check(self) -> bool:
        ...
