from urllib.parse import urlparse

import requests

from src.domain.entities import ContextItem, ProviderConfig
from src.domain.exceptions import (
    AuthenticationError,
    ItemNotFoundError,
    ProviderServerError,
)
from src.domain.interfaces import ProviderInterface
from src.infrastructure.builders.context_item import ContextItemBuilder


class YouTrackProvider(ProviderInterface):
    def __init__(self, config: ProviderConfig) -> None:
        self._config = config

    # ════════ ZONA PÚBLICA ════════

    def get_item(self, item_id: str, config: ProviderConfig) -> ContextItem:
        """Obtiene un issue de YouTrack y retorna ContextItem."""
        self._validate_base_url(config)
        url = f"{config.base_url}/api/issues/{item_id}"
        headers = {"Authorization": f"Bearer {config.token}"}
        params = {"fields": "id,idReadable,summary,description"}
        response = requests.get(url, params=params, headers=headers, timeout=30)
        self._handle_http_errors(response)
        data = response.json()
        return self._build_context_item(item_id, data)

    def validate_config(self, config: ProviderConfig) -> bool:
        """Valida que token y URL sean válidos."""
        return bool(config.token) and self._is_valid_url(config.base_url)

    # ════════ ZONA PRIVADA ════════

    def _validate_base_url(self, config: ProviderConfig) -> None:
        """Lanza error si base_url es None."""
        if config.base_url is None:
            raise ProviderServerError("base_url is required")

    def _handle_http_errors(self, response: requests.Response) -> None:
        """Mapea códigos HTTP a excepciones."""
        if response.status_code in (401, 403):
            raise AuthenticationError("YouTrack auth failed")
        if response.status_code == 404:
            raise ItemNotFoundError("YouTrack issue not found")
        if response.status_code >= 500:
            raise ProviderServerError("YouTrack server error")

    def _build_context_item(self, item_id: str, data: dict) -> ContextItem:
        """Construye ContextItem con ContextItemBuilder."""
        return (
            ContextItemBuilder()
            .set_item_id(item_id)
            .set_provider_name("youtrack")
            .set_title(data.get("summary", ""))
            .set_description(data.get("description", ""))
            .set_comments([])
            .set_custom_fields({})
            .build()
        )

    def _is_valid_url(self, url: str | None) -> bool:
        """Verifica formato de URL."""
        if not url:
            return False
        try:
            parsed = urlparse(url)
            return parsed.scheme in ("http", "https") and bool(parsed.netloc)
        except Exception:
            return False
