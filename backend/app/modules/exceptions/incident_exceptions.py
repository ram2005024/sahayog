from typing import Any

from app.exceptions.custom_base_exception import AppException


class IncidentIdempotancyKeyMissing(AppException):
    def __init__(
        self,
        message: str = "Incident idempotancy key is missing",
        status_code: int = 400,
        details: Any | None = None,
        error_code: str | None = "MISSING_KEY",
    ) -> None:
        super().__init__(message, status_code, details, error_code)
