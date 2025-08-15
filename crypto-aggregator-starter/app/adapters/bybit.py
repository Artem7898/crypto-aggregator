import asyncio
import json
import websockets  # type: ignore
from decimal import Decimal
from typing import List
from app.services.cache import get_cache, cache_key_orderbook
from app.models.schemas import OrderBook, Level

BYBIT_SPOT_WS = "wss://stream.bybit.com/v5/public/spot"

def normalize_symbol(symbol: str) -> str:
    if "-" in symbol:
        return symbol.upper()
    return f"{symbol[:-4]}-{symbol[-4:]}"

async def store_orderbook(symbol: str, exchange: str, bids: List[List[str]], asks: List[List[str]]):
    ob = OrderBook(
        symbol=normalize_symbol(symbol),
        exchange=exchange,
        bids=[Level(price=Decimal(b[0]), qty=Decimal(b[1])) for b in bids],
        asks=[Level(price=Decimal(a[0]), qty=Decimal(a[1])) for a in asks],
        depth=min(len(bids), len(asks), 50),
    )
    cache = get_cache()
    await cache.set(cache_key_orderbook(ob.symbol, exchange), ob.model_dump_json(), ttl=2)

async def run_orderbook_stream(symbol: str = "BTCUSDT"):
    sub_msg = {"op": "subscribe", "args": [f"orderbook.1.{symbol}"]}
    while True:
        try:
            async with websockets.connect(BYBIT_SPOT_WS, ping_interval=20, ping_timeout=20) as ws:
                await ws.send(json.dumps(sub_msg))
                async for raw in ws:
                    msg = json.loads(raw)
                    if "data" in msg and isinstance(msg["data"], dict):
                        data = msg["data"]
                        bids = data.get("b", [])
                        asks = data.get("a", [])
                        if bids and asks:
                            await store_orderbook(symbol, "bybit", bids, asks)
        except Exception:
            await asyncio.sleep(3)

