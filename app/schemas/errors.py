from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str

    model_config = {"json_schema_extra": {"example": {"message": "Descripción del error"}}}
