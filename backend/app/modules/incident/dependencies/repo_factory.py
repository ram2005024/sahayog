from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_db
from app.modules.incident.repos.incident_repo import IncidentRepo


# Incident repo
def get_incident_repo(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return IncidentRepo(db)
