from app.modules.incident.schemas.incident import (
    FoodSchema,
    MedicalSchema,
    OthersSchema,
    RescueSchema,
    ShelterSchema,
)

Details = RescueSchema | MedicalSchema | FoodSchema | OthersSchema | ShelterSchema
