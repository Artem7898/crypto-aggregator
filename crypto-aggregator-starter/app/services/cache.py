import time
from typing import Optional
from app.core.config import settings

try:
    import redis.asyncio as aioredis  # type: ignore
except Exception:  # pragma: no cover
    aioredis = None  # type: ignore

class BaseCache:
    async def get(self, key: str) -> Optional[str]:
        raise NotImplementedError
    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        raise NotImplementedError

class MemoryCache(BaseCache):
    def __init__(self):
        self._store: dict[str, tuple[str, float | None]] = {}
    async def get(self, key: str) -> Optional[str]:
        val = self._store.get(key)
        if not val:
            return None
        value, exp = val
        if exp is not None and time.time() > exp:
            self._store.pop(key, None)
            return None
        return value
    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        exp = time.time() + ttl if ttl else None
        self._store[key] = (value, exp)

class RedisCache(BaseCache):
    def __init__(self, url: str):
        if aioredis is None:
            raise RuntimeError("redis package not available")
        self._client = aioredis.from_url(url, encoding="utf-8", decode_responses=True)
    async def get(self, key: str) -> Optional[str]:
        return await self._client.get(key)
    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        if ttl:
            await self._client.set(key, value, ex=ttl)
        else:
            await self._client.set(key, value)

_cache: BaseCache | None = None

def get_cache() -> BaseCache:
    global _cache
    if _cache is not None:
        return _cache
    if settings.redis_url:
        try:
            _cache = RedisCache(settings.redis_url)
            return _cache
        except Exception:
            pass
    _cache = MemoryCache()
    return _cache

def cache_key_orderbook(symbol: str, exchange: str) -> str:
    return f"orderbook:{symbol}:{exchange}"

