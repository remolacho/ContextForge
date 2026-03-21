from app.schemas import TOOLS_DEFINITION


class ToolsListHandler:
    def execute(self) -> list[dict]:
        return TOOLS_DEFINITION
