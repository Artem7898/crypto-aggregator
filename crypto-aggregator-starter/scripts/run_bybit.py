import asyncio
from app.adapters.bybit import run_orderbook_stream

if __name__ == "__main__":
    asyncio.run(run_orderbook_stream("BTCUSDT"))

