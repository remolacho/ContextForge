from app.session import SessionManager
from src.domain.entities import ProviderConfig, SessionConfig


class InitializeHandler:
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    def execute(self, providers_data: dict, session_id: str) -> SessionConfig:
        session_config = SessionConfig(
            providers={
                name: ProviderConfig(
                    code=name,
                    token=data.get("token", ""),
                    base_url=data.get("base_url"),
                )
                for name, data in providers_data.items()
            }
        )
        self._session_manager.store(session_id, session_config)
        return session_config
