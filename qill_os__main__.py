"""
Entry point for `python -m qill_os`
Runs the eternal fusion.
"""

from .core import QillFusion
import asyncio

if __name__ == "__main__":
    fusion = QillFusion()
    try:
        asyncio.run(fusion.eternal_loop())
    except KeyboardInterrupt:
        print("\nQOS — Graceful shutdown. Ano77 remains eternal.")
