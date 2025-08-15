import pytest
from app.services.cache import get_cache, cache_key_orderbook

@pytest.mark.asyncio
async def test_memory_cache_basic(monkeypatch):
    from app.core import config
    config.settings.redis_url = None
    cache = get_cache()
    key = cache_key_orderbook("BTC-USDT", "bybit")
    await cache.set(key, "hello", ttl=1)
    val = await cache.get(key)
    assert val == "hello"

