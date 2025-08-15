from fastapi import APIRouter, HTTPException, Query
from app.services.cache import get_cache, cache_key_orderbook
from app.models.schemas import OrderBook, CombinedOrderBook
from datetime import datetime, timezone

router = APIRouter()

@router.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}

@router.get("/orderbook")
async def get_orderbook(symbol: str = Query(..., examples=["BTC-USDT"]), exchange: str = "bybit"):
    cache = get_cache()
    data = await cache.get(cache_key_orderbook(symbol.upper(), exchange))
    if not data:
        raise HTTPException(status_code=404, detail="orderbook not available yet")
    ob = OrderBook.model_validate_json(data)
    return ob

@router.get("/orderbook/combined")
async def get_orderbook_combined(symbol: str = Query(..., examples=["BTC-USDT"])):
    cache = get_cache()
    data = await cache.get(cache_key_orderbook(symbol.upper(), "bybit"))
    if not data:
        raise HTTPException(status_code=404, detail="orderbook not available yet")
    ob = OrderBook.model_validate_json(data)
    cob = CombinedOrderBook(symbol=ob.symbol, bids=ob.bids, asks=ob.asks, ts=datetime.now(timezone.utc))
    return cob

@router.get("/exchanges")
async def exchanges():
    return {"bybit": {"connected": True, "lag_ms": 0}}

