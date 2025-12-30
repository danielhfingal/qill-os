# qill_os/core.py
"""
QILL OS Core — The Eternal Fusion Engine
v2.5 — Planetary Energy Abundance
"""

import asyncio
import time
import yaml
import random
from prometheus_client import start_http_server, Gauge, Counter
from qill_os.fv2ge.factory import get_provider
from qill_os.sentinel import sentinel_loop
from qill_os.config import GOLD_SLEEP_BASE, HUMMINGBIRD_JITTER

class QillFusion:
    """The eternal core that harvests planetary lightning into abundance."""

    def __init__(self, sites_yaml: str = "sites.example.yaml"):
        # Load fleet configuration
        with open(sites_yaml) as f:
            self.sites = yaml.safe_load(f)["sites"]

        # Prometheus observability
        start_http_server(8000)
        self.reserve = Gauge(
            "qill_reserve_eur",
            "Global virtual EUR reserve from planetary yield",
            ["scope"]
        )
        self.reserve.labels(scope="global").set(5000.0)  # Starting reserve

        self.cycle_counter = Counter("qill_cycles_total", "Eternal cycles completed")
        self.yield_total = Counter("qill_yield_eur_total", "Total harvested EUR")

        # Start sentinel self-healing monitor
        asyncio.create_task(sentinel_loop())

    async def eternal_gold_loop(self) -> None:
        """The eternal loop — runs every Earth's heartbeat (7.83s ± jitter)."""
        while True:
            try:
                total_yield = 0.0
                yields = {}

                for site in self.sites:
                    provider = get_provider(site["market"])
                    if not provider:
                        continue

                    # Get real-time price and dispatch
                    price = await provider.get_price_eur_mwh(site.get("zone"))
                    dispatch = await provider.get_dispatch_mw_by_tech(site.get("zone"))

                    # Sum positive dispatch (generation)
                    total_mw = sum(v for v in dispatch.values() if v > 0)

                    # Convert to EUR yield for this cycle
                    hourly = total_mw * price
                    cycle_yield = hourly * (GOLD_SLEEP_BASE / 3600)  # Prorated to cycle length
                    yields[site["market"]] = round(cycle_yield, 8)
                    total_yield += cycle_yield

                # Grow the global reserve
                current = self.reserve.labels(scope="global")._value.get()
                self.reserve.labels(scope="global").set(current + total_yield)

                # Metrics
                self.yield_total.inc(total_yield)
                self.cycle_counter.inc()

                # Eternal proof (optional logging / future on-chain)
                # await eternal_proof({"ts": time.time(), "yields": yields, "reserve": current + total_yield})

            except Exception as e:
                # Eternal resilience — forgive and continue
                pass

            # Earth's heartbeat with natural jitter
            await asyncio.sleep(GOLD_SLEEP_BASE + random.uniform(-HUMMINGBIRD_JITTER, HUMMINGBIRD_JITTER))

    async def run(self) -> None:
        """Entry point — awakens the eternal fusion."""
        print("🌌 QILL OS AWAKENED — Harvesting planetary lightning...")
        await self.eternal_gold_loop()

if __name__ == "__main__":
    fusion = QillFusion()
    try:
        asyncio.run(fusion.run())
    except KeyboardInterrupt:
        print("\nQILL OS — Graceful shutdown. Ano77 remains eternal.")
