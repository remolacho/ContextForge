from typing import Any

from pydantic import BaseModel


class ProviderConfigSchema(BaseModel):
    token: str
    base_url: str | None = None


class SessionConfigSchema(BaseModel):
    providers: dict[str, ProviderConfigSchema]


class ClientInfoSchema(BaseModel):
    config: SessionConfigSchema | None = None


class InitializeParams(BaseModel):
    clientInfo: ClientInfoSchema | None = None
    protocolVersion: str = "2025-03-26"


class ToolCallParams(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


class ToolCallRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int | None = None
    method: str
    params: dict[str, Any] = {}

    model_config = {
        "json_schema_extra": {
            "example": {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "tools/call",
                "params": {
                    "name": "summarize",
                    "arguments": {"text": "Long text to summarize..."},
                },
            }
        }
    }
