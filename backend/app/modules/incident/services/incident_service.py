from app.modules.incident.repos.incident_repo import IncidentRepo
from app.modules.incident.schemas.incident import IncidentCreateSchema


class IncidentService:
    def __init__(self, incident_repo: IncidentRepo) -> None:
        self.incident_repo = incident_repo

    # Services will come here
    async def create_incident_service(self, data: IncidentCreateSchema):
        return await self.incident_repo.create_incident(data)
