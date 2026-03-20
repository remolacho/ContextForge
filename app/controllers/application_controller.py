from fastapi import APIRouter


class ApplicationController:
    def __init__(self, router: APIRouter) -> None:
        self.router = router
