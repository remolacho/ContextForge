from app.schemas.mcp_response import ItemResponse, ToolCallResponse
from src.domain.entities import CacheEntry, Chunk


def serialize_response(result: CacheEntry | list[Chunk]) -> dict:
    if isinstance(result, CacheEntry):
        return ToolCallResponse(items=[ItemResponse(index=1, content=result.content)]).model_dump()

    chunks: list[Chunk] = result
    return ToolCallResponse(
        items=[ItemResponse(index=c.chunk_index, content=c.content) for c in chunks]
    ).model_dump()
