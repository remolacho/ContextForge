from src.domain.entities import ProviderConfig
from src.domain.exceptions import ProviderNotRegisteredError
from src.domain.interfaces import ProviderInterface
from src.infrastructure.providers.task.youtrack import YouTrackProvider


class ProviderFactory:
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def create(self) -> ProviderInterface:
        code = self.config.code
        if code == "youtrack":
            return YouTrackProvider(self.config)
        raise ProviderNotRegisteredError(
            f"Proveedor '{code}' no reconocido. Disponibles: youtrack"
        )
