from abc import ABC, abstractmethod
from .entities import ContextItem, ProviderConfig, CacheEntry, Chunk, LLMConfig


class ProviderInterface(ABC):
    @abstractmethod
    def get_item(self, item_id: str, config: ProviderConfig) -> ContextItem: ...

    @abstractmethod
    def validate_config(self, config: ProviderConfig) -> bool: ...


class CacheRepositoryInterface(ABC):
    @abstractmethod
    def lookup(self, item_id: str, provider_name: str, content_hash: str, tool: str, **kwargs) -> CacheEntry | None: ...

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
