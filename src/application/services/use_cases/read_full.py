from datetime import datetime, timezone

from src.domain.entities import CacheEntry
from src.domain.interfaces import CacheRepositoryInterface, ProviderInterface
from src.infrastructure.builders.cache_entry import CacheEntryBuilder


class ReadFullUseCase:
    def __init__(
        self,
        provider: ProviderInterface,
        cache: CacheRepositoryInterface,
    ) -> None:
        self._provider = provider
        self._cache = cache

    def execute(self, item_id: str, provider_name: str) -> CacheEntry:
        item = self._provider.get_item(item_id, self._provider._config)  # type: ignore[attr-defined]

        cached = self._cache.lookup(item_id, provider_name, item.content_hash, "read_full")
        if cached:
            return cached

        entry = (
            CacheEntryBuilder()
            .for_item(item)
            .with_tool("read_full")
            .with_content(item.raw_content)
            .with_metadata(timestamp=datetime.now(timezone.utc).isoformat())
            .build()
        )
        self._cache.store(entry)
        return entry
