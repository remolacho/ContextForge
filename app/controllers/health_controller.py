from app.controllers.application_controller import ApplicationController


class HealthController(ApplicationController):
    def __init__(self, router) -> None:
        super().__init__(router)
        self.router.tags = ["Health"]

        @self.router.get("/health", summary="Check Server Health")
        async def health():
            """Returns the current operational status of the server."""
            return {"status": "ok"}
