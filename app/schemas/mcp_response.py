from pydantic import BaseModel


class ItemResponse(BaseModel):
    index: int
    content: str


class ToolCallResponse(BaseModel):
    items: list[ItemResponse]
