from src.domain.entities import SessionConfig
from src.domain.exceptions import SessionConfigError


class SessionManager:
    _sessions: dict[str, SessionConfig] = {}

    def store(self, session_id: str, config: SessionConfig) -> None:
        self._validate(config)
        self._sessions[session_id] = config

    def get(self, session_id: str) -> SessionConfig:
        if session_id not in self._sessions:
            raise SessionConfigError("Sesión no encontrada. Llama a initialize primero.")
        return self._sessions[session_id]

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def _validate(self, config: SessionConfig) -> None:
        if not config.providers:
            raise SessionConfigError("La sesión debe tener al menos un proveedor")
        for name, provider_config in config.providers.items():
            if not provider_config.token or not provider_config.token.strip():
                raise SessionConfigError(f"El token del proveedor '{name}' no puede estar vacío")
