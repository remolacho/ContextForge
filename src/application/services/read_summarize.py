from datetime import datetime, timezone

from src.domain.entities import CacheEntry
from src.domain.exceptions import ValidationError
from src.domain.interfaces import (
    CacheRepositoryInterface,
    ProviderInterface,
    SummarizeEngineInterface,
)
from src.infrastructure.builders.cache_entry import CacheEntryBuilder


class ReadSummarizeUseCase:
    def __init__(
        self,
        provider: ProviderInterface,
        cache: CacheRepositoryInterface,
        summarized: SummarizeEngineInterface,
    ) -> None:
        self._provider = provider
        self._cache = cache
        self._summarized = summarized

    def execute(
        self,
        item_id: str,
        provider_name: str,
        max_tokens: int = 500,
    ) -> CacheEntry:
        if not (1 <= max_tokens <= 10000):
            raise ValidationError("max_tokens debe estar entre 1 y 10000")

        item = self._provider.get_item(item_id, self._provider._config)  # type: ignore[attr-defined]

        cached = self._cache.lookup(
            item_id, provider_name, item.content_hash, "read_summarize", max_tokens=max_tokens
        )
        if cached:
            return cached

        summary = self._summarized.summarize(item.raw_content, max_tokens)

        entry = (
            CacheEntryBuilder()
            .for_item(item)
            .with_tool("read_summarize")
            .with_content(summary)
            .with_metadata(max_tokens=max_tokens, timestamp=datetime.now(timezone.utc).isoformat())
            .build()
        )
        self._cache.store(entry)
        return entry
