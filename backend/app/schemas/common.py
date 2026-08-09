from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):  # noqa: UP046
    success: bool = True
    message: str | None = None
    data: T | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Any | None = None
    error_code: str | None = None
