from app.modules.incident.schemas.incident_category_schema import (
    FoodSchema,
    MedicalSchema,
    OthersSchema,
    RescueSchema,
    ShelterSchema,
)

Details = RescueSchema | MedicalSchema | FoodSchema | OthersSchema | ShelterSchema
