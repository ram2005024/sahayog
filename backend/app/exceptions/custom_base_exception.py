from typing import Any


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.details = details
        self.message = message
        self.error_code = error_code
        super().__init__(message)
