from typing import Literal

from pydantic import BaseModel, Field, field_validator


class IncidentSignatureRequest(BaseModel):
    file_length: int = Field(
        ...,
        ge=0,
        le=4,
    )
    file_types: list[Literal["image", "audio"]] = Field(..., min_length=0, max_length=4)

    @field_validator("file_types")
    @classmethod
    def normalize_file_types(cls, value):
        has_more_images = value.count("image") > 3
        has_more_audio = value.count("audio") > 1
        if has_more_images:
            raise ValueError("You can upload maximum 3 images")
        if has_more_audio:
            raise ValueError("You can upload maximum 1 audio")
        return value


class SingleSignatureResponse(BaseModel):
    signature: str
    url: str
    timestamp: int
    public_id: str
    api_key: str
    upload_preset: str


class SignatureResponse(BaseModel):
    signatures: list[SingleSignatureResponse]
    exp_time: int = 60


class MediaMetaData(BaseModel):
    public_id: str
    url: str
    format: str
    size: float
    width: int
    height: int


class IncidentMediaSchema(BaseModel):
    type: Literal["image", "audio"]
    url: str
    meta_data: MediaMetaData
