"""Tests para ReadFullUseCase."""

from unittest.mock import MagicMock

from src.application.use_cases.read_full import ReadFullUseCase
from src.domain.entities import CacheEntry, ContextItem


def test_cache_hit_returns_cached_entry():
    """Cuando hay cache hit, retorna la entrada cacheada."""
    provider = MagicMock()
    cache = MagicMock()
    item = ContextItem(
        item_id="1",
        provider_name="youtrack",
        title="Test",
        description="Description",
        comments=[],
        custom_fields={},
        raw_content="raw content",
        content_hash="abc123",
    )
    cached_entry = CacheEntry(
        item_id="1",
        provider_name="youtrack",
        content_hash="abc123",
        tool="read_full",
        content="cached content",
        metadata={},
        from_cache=True,
    )
    provider.get_item.return_value = item
    cache.lookup.return_value = cached_entry

    use_case = ReadFullUseCase(provider=provider, cache=cache)
    result = use_case.execute("1", "youtrack")

    assert result.from_cache is True
    assert result.content == "cached content"
    cache.store.assert_not_called()


def test_cache_miss_generates_and_stores():
    """Cuando hay cache miss, genera entrada y la guarda."""
    provider = MagicMock()
    cache = MagicMock()
    item = ContextItem(
        item_id="1",
        provider_name="youtrack",
        title="Test",
        description="Description",
        comments=[],
        custom_fields={},
        raw_content="raw content",
        content_hash="abc123",
    )
    provider.get_item.return_value = item
    cache.lookup.return_value = None

    use_case = ReadFullUseCase(provider=provider, cache=cache)
    result = use_case.execute("1", "youtrack")

    assert result.from_cache is False
    assert result.content == "raw content"
    cache.store.assert_called_once()


def test_provider_always_called():
    """Provider siempre es llamado primero para datos frescos."""
    provider = MagicMock()
    cache = MagicMock()
    item = ContextItem(
        item_id="1",
        provider_name="youtrack",
        title="Test",
        description="Description",
        comments=[],
        custom_fields={},
        raw_content="raw content",
        content_hash="abc123",
    )
    provider.get_item.return_value = item
    cache.lookup.return_value = None

    use_case = ReadFullUseCase(provider=provider, cache=cache)
    use_case.execute("1", "youtrack")

    provider.get_item.assert_called_once()
    call_args = provider.get_item.call_args
    assert call_args[0][0] == "1"
