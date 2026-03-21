from fastapi import status

from app.controllers.application_controller import ApplicationController
from app.handlers.initialize import InitializeHandler
from app.handlers.tool_call import ToolCallHandler
from app.handlers.tools_list import ToolsListHandler
from app.schemas import ErrorResponse, ToolCallRequest
from app.schemas.serialize import serialize_response
from app.session import SessionManager
from src.application.services.context_service import ContextService


class MCPController(ApplicationController):
    def __init__(
        self,
        router,
        context_service: ContextService,
        session_manager: SessionManager,
    ) -> None:
        super().__init__(router)
        self.router.tags = ["MCP"]
        self._context_service = context_service
        self._session_manager = session_manager

        @self.router.post(
            "/",
            status_code=status.HTTP_200_OK,
            summary="Handle MCP Protocol Messages",
            description=(
                "Process Model Context Protocol (MCP) requests "
                "including initialize, tools/list, and tools/call."
            ),
            responses={
                400: {"model": ErrorResponse, "description": "Método desconocido"},
                422: {"model": ErrorResponse, "description": "Error de dominio"},
            },
        )
        async def handle_mcp(request: ToolCallRequest):
            """
            Handles incoming JSON-RPC style messages for MCP operations.
            - `initialize`: Initialize session and providers.
            - `tools/list`: List all available tools.
            - `tools/call`: Execute a specific tool with parameters.
            """
            if request.method == "initialize":
                providers = (
                    request.params.get("clientInfo", {}).get("config", {}).get("providers", {})
                )
                InitializeHandler(self._session_manager).execute(
                    providers_data=providers,
                    session_id=str(request.id or "default"),
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "result": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "serverInfo": {"name": "contextforge", "version": "1.0.0"},
                    },
                }

            if request.method == "tools/list":
                result = ToolsListHandler().execute()
                return {
                    "jsonrpc": "2.0",
                    "id": None,
                    "result": {"tools": result},
                }

            if request.method == "tools/call":
                params = request.params
                session = self._session_manager.get(str(request.id or "default"))
                tool_result = ToolCallHandler(self._context_service, self._session_manager).execute(
                    tool_name=params["name"],
                    arguments=params.get("arguments", {}),
                    session=session,
                )
                return serialize_response(tool_result)

            return {"message": f"Método '{request.method}' no soportado"}

        @self.router.get(
            "/",
            status_code=status.HTTP_200_OK,
            summary="SSE Connection Status",
            description="Returns status information for the Server-Sent Events (SSE) connection.",
        )
        async def mcp_sse():
            """Check the status of the SSE communication channel."""
            return {"message": "SSE endpoint activo"}
