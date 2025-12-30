from prometheus_client import Gauge
from qill_os.fv2ge.factory import PROVIDERS
import asyncio

health_gauge = Gauge("qill_provider_health", "Provider health 1=ok 0=fail", ["market"])

async def sentinel_loop(interval_hours: float = 4.0):
    while True:
        for market, provider in PROVIDERS.items():
            try:
                healthy = await asyncio.wait_for(provider.health_check(), timeout=15)
                health_gauge.labels(market=market).set(1 if healthy else 0)
            except:
                health_gauge.labels(market=market).set(0)
        await asyncio.sleep(interval_hours * 3600)
