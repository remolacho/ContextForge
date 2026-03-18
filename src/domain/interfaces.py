from abc import ABC, abstractmethod

from .entities import CacheEntry, ContextItem, ProviderConfig


class ProviderInterface(ABC):
    @abstractmethod
    def get_item(self, item_id: str, config: ProviderConfig) -> ContextItem: ...

    @abstractmethod
    def validate_config(self, config: ProviderConfig) -> bool: ...


class CacheRepositoryInterface(ABC):
    @abstractmethod
    def lookup(
        self, item_id: str, provider_name: str, content_hash: str, tool: str, **kwargs
    ) -> CacheEntry | None:
        """Busca en caché por item_id + provider_name + content_hash + tool + params adicionales.

        Args:
            item_id: ID del ítem en el proveedor
            provider_name: Nombre del proveedor (ej. "youtrack")
            content_hash: SHA-256 del raw_content del ContextItem (requerido)
            tool: Tool solicitado ("read_full", "read_summarize", "read_chunks")
            **kwargs: Parámetros adicionales como max_tokens para summarize

        Returns:
            CacheEntry si hay hit, None si hay miss
        """
        ...

    @abstractmethod
    def store(self, entry: CacheEntry) -> None: ...

    @abstractmethod
    def invalidate(self, item_id: str, provider_name: str, tool: str) -> None: ...


class LLMEngineInterface(ABC):
    @abstractmethod
    def summarize(self, content: str, max_tokens: int) -> str: ...

    @abstractmethod
    def count_tokens(self, text: str) -> int: ...

    @abstractmethod
    def get_embeddings(self, text: str) -> list[float]: ...
