# Crypto Aggregator (Starter)

FastAPI-based **order book aggregator** starter: one working connector (Bybit), cache with Redis or in-memory fallback, REST endpoints, Prometheus metrics, tests, and Docker.

> Goal: extend to multiple exchanges (OKX, Binance, KuCoin, Bitget), add WS streaming, and deploy on AWS App Runner.

---

## Features
- **FastAPI** HTTP API: `/healthz`, `/orderbook`, `/orderbook/combined`, `/exchanges`, `/metrics`
- **Connector (Bybit)** minimal WS reader (demo) → normalized order book → cache (TTL 2s)
- **Cache**: Redis (if `REDIS_URL` set) or in-memory fallback
- **Metrics**: Prometheus counters & histograms
- **Tests**: pytest + async client
- **Docker & Compose**: app + Redis
- **CI skeleton** and **AWS App Runner** checklist

## Local Run (Ubuntu)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install .[dev]

# Run API
make run

# (Optional) run connector in a separate shell to populate cache
python - <<'PY'
import asyncio
from app.adapters.bybit import run_orderbook_stream
asyncio.run(run_orderbook_stream("BTCUSDT"))
PY

# Tests
make test
```

Or with Docker:
```bash
cp .env.example .env
docker compose up --build
```

## API Examples
- `GET /healthz`
- `GET /orderbook?symbol=BTC-USDT&exchange=bybit`
- `GET /orderbook/combined?symbol=BTC-USDT`
- `GET /exchanges`
- `GET /metrics`

## Roadmap
- [ ] Add connectors: OKX, Binance, KuCoin, Bitget
- [ ] WS endpoint for real-time updates
- [ ] Normalize lot/price tick, depth=50 aggregation
- [ ] Prometheus → Grafana dashboard
- [ ] CI/CD → AWS ECR + App Runner
- [ ] SLOs (p95 latency < 50ms from cache), alerts

## License
MIT

