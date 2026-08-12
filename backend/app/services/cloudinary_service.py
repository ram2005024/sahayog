import hashlib
import time
import uuid

from app.core.config import settings
from app.schemas.media_schema import (
    IncidentSignatureRequest,
    SignatureResponse,
    SingleSignatureResponse,
)


class CloudinaryService:
    def __init__(self) -> None:
        pass

    # Services will come here

    def select_incident_media_preset(self, value):
        return "incident_image_preset" if value == "image" else "incident_audio_preset"

    def generate_signatures_for_incident_medias(
        self, user_id: str, data: IncidentSignatureRequest
    ):
        signatures = []
        for _, value in enumerate(data.file_types):
            media_preset = self.select_incident_media_preset(value)
            unique_id = str(uuid.uuid4())
            public_id = f"incident/user_{user_id}/{value}/{unique_id}"
            timestamp = time.time()
            cloud_name = settings.CLOUD_NAME
            params = "&".join(
                [
                    f"public_id={public_id}",
                    f"preset={media_preset}",
                    f"timestamp={timestamp}",
                ]
            )
            raw = params + settings.CLOUD_SECRET
            signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            url = f"https://api.cloudinary.com/v1_1/{cloud_name}/auto/upload"
            signatures.append(
                SingleSignatureResponse(
                    timestamp=int(timestamp),
                    public_id=public_id,
                    cloud_name=cloud_name,
                    api_key=settings.CLOUD_KEY,
                    signature=signature,
                    url=url,
                ).model_dump()
            )
        return SignatureResponse(signatures=signatures)
