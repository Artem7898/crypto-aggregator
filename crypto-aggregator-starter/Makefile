.PHONY: run test lint format docker-build compose

run:
	uvicorn app.api.main:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check . && mypy app

format:
	ruff check . --fix

docker-build:
	docker build -t crypto-aggregator:local .

compose:
	docker compose up --build

