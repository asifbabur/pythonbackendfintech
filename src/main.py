from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.endpoints.customers import router as customer_router
from src.core.config import get_settings
from src.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(title=get_settings().app_name, lifespan=lifespan)

app.include_router(customer_router)
