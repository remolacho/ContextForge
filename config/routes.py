from fastapi import APIRouter

from app.controllers.health_controller import HealthController
from app.controllers.mcp_controller import MCPController


class Routes:
    def __init__(self, app, **deps) -> None:
        self._app = app
        self._deps = deps

    def register(self) -> None:
        router = APIRouter(responses={404: {"description": "Not found"}})

        self._app.include_router(
            MCPController(router, **self._deps).router,
            prefix="/mcp",
        )

        self._app.include_router(HealthController(router).router)
