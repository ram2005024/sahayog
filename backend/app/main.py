from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # Noqa
from app.apis.base_router import include_base_router
from app.core.startup import startup_redis
from app.exceptions.exception_handler import exception_handler_caller
from app.middlewares.logger_middleware import LoggingMiddleware


# LIFE SPAN
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with startup_redis(app):
        yield


app = FastAPI(title="sahayog", lifespan=lifespan)


include_base_router(app)
exception_handler_caller(app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)
