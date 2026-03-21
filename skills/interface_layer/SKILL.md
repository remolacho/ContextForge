# Interface Layer (FastAPI, Controllers, Handlers, and Schemas)

The Interface Layer is responsible for handling communication with the outside world using the Model Context Protocol (MCP) and FastAPI.

## 1. FastAPI Pattern
The application follows a modular and class-based FastAPI structure. 
- `main.py`: Entry point that creates the FastAPI app, registers global exception handlers, and mounts routers.
- `config/routes.py`: Mounts `APIRouter` instances into the main application.

## 2. Controllers and Handlers
- **`ApplicationController` (Base)**: Inherits from `APIRouter` and sets up the foundational routing mechanism.
- **`MCPController`**: A lightweight controller that orchestrates MCP requests. It handles three primary MCP methods:
  - `initialize`: Configure session and providers.
  - `tools/list`: List available tools.
  - `tools/call`: Execute tool functionality.
- **`Handlers` (Strategy Pattern)**: Each MCP method has its own handler (`InitializeHandler`, `ToolsListHandler`, `ToolCallHandler`) to encapsulate business logic apart from request/response structures.

## 3. Schemas and Serialization
- **Pydantic Models**: Used for request/response validation (`mcp_request.py`, `mcp_response.py`).
- **Serialization**: `serialize_response()` is responsible for transforming Domain objects to JSON-RPC-compliant dictionaries.
- **Global Error Handling**: Centralized exception handlers catch domain-specific exceptions and return consistent JSON error responses.

## 4. MCP Streamable HTTP Support
The server supports the Model Context Protocol (MCP) via HTTP, exposing three tools (`read_full`, `read_summarize`, `read_chunks`) that facilitate token-efficient context retrieval for AI agents.
