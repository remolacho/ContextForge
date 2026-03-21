from abc import ABC, abstractmethod
from typing import Any

from app.schemas.mcp_request import ToolCallRequest


class MCPHandler(ABC):
    @abstractmethod
    async def handle(self, request: ToolCallRequest) -> Any: ...

    def _get_session_id(self, request: ToolCallRequest) -> str:
        return str(request.id) if request.id else "default"
