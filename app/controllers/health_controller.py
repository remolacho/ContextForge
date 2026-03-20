from app.controllers.application_controller import ApplicationController


class HealthController(ApplicationController):
    def __init__(self, router) -> None:
        super().__init__(router)
        self.router.tags = ["Health"]

        @self.router.get("/health")
        async def health():
            return {"status": "ok"}
