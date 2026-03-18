from src.domain.entities import ContextItem, ProviderConfig
from src.domain.interfaces import ProviderInterface


class YouTrackProvider(ProviderInterface):
    def __init__(self, config: ProviderConfig) -> None:
        self._config = config

    def get_item(self, item_id: str, config: ProviderConfig) -> ContextItem:
        raise NotImplementedError("YouTrackProvider no implementado aún")

    def validate_config(self, config: ProviderConfig) -> bool:
        raise NotImplementedError("YouTrackProvider no implementado aún")
