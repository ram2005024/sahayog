from fastapi import Request

from app.modules.exceptions.incident_exceptions import IncidentIdempotancyKeyMissing


def get_idempotancy_key(request: Request):
    key = request.headers.get("incident_idempotancy_key")
    if not key:
        raise IncidentIdempotancyKeyMissing
    return key
