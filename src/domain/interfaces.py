from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol

from .entities import CacheEntry, ContextItem, ProviderConfig


class LLM(Protocol):
    def get_num_tokens(self, text: str) -> int: ...
    def invoke(self, input: Any) -> Any: ...
    def __or__(self, other: Any) -> Any: ...


class Embeddings(Protocol):
    def embed_query(self, text: str) -> list[float]: ...


class LLMEngineInterface(ABC):
    @property
    @abstractmethod
    def llm(self) -> LLM: ...

    @property
    @abstractmethod
    def embeddings(self) -> Embeddings: ...


class TokenizerInterface(ABC):
    @abstractmethod
    def count_tokens(self, text: str) -> int: ...


class TextProcessingInterface(ABC):
    @abstractmethod
    def summarize(self, content: str, max_tokens: int) -> str: ...

    @abstractmethod
    def count_tokens(self, text: str) -> int: ...

    @abstractmethod
    def get_embeddings(self, text: str) -> list[float]: ...


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
