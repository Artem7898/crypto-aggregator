# Architecture

## Data Flow
Exchanges (WS/REST) → adapters (normalize) → cache (Redis/in-memory) → API (REST/WS) → clients

## Modules
- `app/adapters`: exchange connectors (Bybit now)
- `app/services/cache.py`: cache abstraction + Redis/memory
- `app/models/schemas.py`: Pydantic models (OrderBook, Level, CombinedOrderBook)
- `app/api`: FastAPI app and routes

## Decisions
- Redis for cache (TTL 2s), memory fallback for local dev
- Prometheus metrics via `/metrics`
- Tests: health, models, cache
- Docker & Compose for local run

