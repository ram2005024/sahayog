from typing import Literal

from pydantic import BaseModel, Field, field_validator


class IncidentSignatureRequest(BaseModel):
    file_length: int = Field(
        ...,
        ge=0,
        le=3,
    )
    file_types: list[Literal["image", "audio"]] = Field(..., min_length=0, max_length=4)

    @field_validator("field_types")
    @classmethod
    def normalize_file_types(cls, value):
        has_more_images = value.count("image") > 3
        has_more_audio = value.count("audio") > 1
        if has_more_images:
            raise ValueError("You can upload maximum of 3 images")
        if has_more_audio:
            raise ValueError("You can upload maximum of 1 audio")
        return value


class SingleSignatureResponse(BaseModel):
    signature: str
    url: str
    timestamp: int
    public_id: str
    api_key: str
    cloud_name: str


class SignatureResponse(BaseModel):
    signatures: list[SingleSignatureResponse]
    exp_time: int = 60
