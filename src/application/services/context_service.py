"""ContextService: Fachada que simplifica el acceso a los casos de uso."""

from src.application.services.use_cases.read_chunks import ReadChunksUseCase
from src.application.services.use_cases.read_full import ReadFullUseCase
from src.application.services.use_cases.read_summarize import ReadSummarizeUseCase
from src.domain.entities import CacheEntry, Chunk, SessionConfig
from src.domain.exceptions import SessionConfigError
from src.domain.interfaces import (
    CacheRepositoryInterface,
    TextProcessingInterface,
    TokenizerInterface,
)
from src.infrastructure.providers.factory import ProviderFactory


class ContextService:
    """Fachada que simplifica el acceso a los casos de uso desde los controllers."""

    def __init__(
        self,
        cache: CacheRepositoryInterface,
        summarized: TextProcessingInterface,
        tokenizer: TokenizerInterface,
    ) -> None:
        self._cache = cache
        self._summarized = summarized
        self._tokenizer = tokenizer

    def read_full(self, item_id: str, provider_name: str, session: SessionConfig) -> CacheEntry:
        self._validate_provider(provider_name, session)
        provider_config = session.providers[provider_name]
        provider = ProviderFactory(provider_config).create()
        return ReadFullUseCase(provider=provider, cache=self._cache).execute(
            item_id=item_id,
            provider_name=provider_name,
        )

    def read_summarize(
        self,
        item_id: str,
        provider_name: str,
        session: SessionConfig,
        max_tokens: int = 500,
    ) -> CacheEntry:
        self._validate_provider(provider_name, session)
        provider_config = session.providers[provider_name]
        provider = ProviderFactory(provider_config).create()
        return ReadSummarizeUseCase(
            provider=provider,
            cache=self._cache,
            summarized=self._summarized,
        ).execute(
            item_id=item_id,
            provider_name=provider_name,
            max_tokens=max_tokens,
        )

    def read_chunks(
        self,
        item_id: str,
        provider_name: str,
        session: SessionConfig,
        chunk_indices: list[int] | None = None,
    ) -> list[Chunk]:
        self._validate_provider(provider_name, session)
        provider_config = session.providers[provider_name]
        provider = ProviderFactory(provider_config).create()
        return ReadChunksUseCase(
            provider=provider,
            cache=self._cache,
            tokenizer=self._tokenizer,
        ).execute(
            item_id=item_id,
            provider_name=provider_name,
            chunk_indices=chunk_indices,
        )

    def _validate_provider(self, provider_name: str, session: SessionConfig) -> None:
        if provider_name not in session.providers:
            available = ", ".join(session.providers.keys())
            raise SessionConfigError(
                f"Proveedor '{provider_name}' no configurado en la sesión. Disponibles: {available}"
            )
