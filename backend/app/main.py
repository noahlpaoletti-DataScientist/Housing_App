from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    investment_routes,
    market_routes,
    property_routes,
    renovation_routes,
    report_routes,
    valuation_routes,
)
from app.config import settings
from app.db.seed import seed_database
from app.db.session import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(property_routes.router, prefix=settings.api_v1_prefix)
app.include_router(valuation_routes.router, prefix=settings.api_v1_prefix)
app.include_router(renovation_routes.router, prefix=settings.api_v1_prefix)
app.include_router(market_routes.router, prefix=settings.api_v1_prefix)
app.include_router(investment_routes.router, prefix=settings.api_v1_prefix)
app.include_router(report_routes.router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
