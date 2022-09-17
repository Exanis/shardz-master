"""
Main application file
"""
import logging
from fastapi import FastAPI
from .routers import authentication_router, servers_router
from .settings import settings


app = FastAPI(
    debug=settings.debug,
    title="Shardz master server",
    description="Master server for Shardz cluster",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)
app.include_router(authentication_router)
app.include_router(servers_router)


@app.on_event("startup")
async def startup():
    """Initialize logging and check application key"""
    logging.basicConfig(level=logging.DEBUG if settings.debug else logging.WARNING)
    if settings.api_key == "invalid_key" and not settings.debug:
        raise RuntimeError("API key is invalid, you must change it in settings.py")
    logging.warning("Server started.")
