from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from starlette.responses import Response
from app.core.config import settings
from app.api.routes import router as api_router

REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["path", "method"])
REQUEST_LATENCY = Histogram("api_latency_seconds", "API request latency seconds", ["path"])

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    path = request.url.path
    method = request.method
    with REQUEST_LATENCY.labels(path=path).time():
        response = await call_next(request)
    REQUEST_COUNT.labels(path=path, method=method).inc()
    return response

app.include_router(api_router)

@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

