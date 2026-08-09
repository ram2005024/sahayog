from fastapi import FastAPI

from app.apis.base_router import include_base_router
from app.exceptions.exception_handler import exception_handler_caller
from app.middlewares.logger_middleware import LoggingMiddleware

app = FastAPI(title="sahayog")

include_base_router(app)
exception_handler_caller(app)
app.add_middleware(LoggingMiddleware)
