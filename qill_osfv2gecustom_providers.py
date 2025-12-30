from .providers import DispatchProvider
import httpx
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# Example sovereign shield — add all your custom ones here
class MIBEL_ESIOSProvider(DispatchProvider):
    def __init__(self):
        self.token = os.getenv("ESIOS_TOKEN")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential())
    async def get_price_eur_mwh(self, zone=None) -> float:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"https://api.esios.ree.es/indicators/600?token={self.token}")
            return resp.json()["values"][0]["value"]

    async def get_dispatch_mw_by_tech(self, zone=None) -> Dict[str, float]:
        # Implement real dispatch fetch
        return {"solar": 1000.0, "wind": 2000.0}

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://api.esios.ree.es/archives/70/download_json?token={self.token}")
                return resp.status_code == 200
        except:
            return False
