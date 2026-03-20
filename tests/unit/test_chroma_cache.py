from unittest.mock import MagicMock, patch

import pytest

from src.domain.entities import CacheEntry
from src.infrastructure.cache.chroma import ChromaCacheRepository


@pytest.fixture
def mock_collection():
    return MagicMock()


@pytest.fixture
def mock_client(mock_collection):
    with patch("chromadb.HttpClient") as mock:
        mock.return_value.get_or_create_collection.return_value = mock_collection
        yield mock


@pytest.fixture
def cache(mock_client, mock_collection):
    return ChromaCacheRepository(host="localhost", port=8000)


def test_lookup_cache_hit(cache, mock_collection):
    """lookup() retorna CacheEntry con from_cache=True cuando ChromaDB tiene documento."""
    mock_collection.get.return_value = {
        "documents": ["contenido cacheado"],
        "metadatas": [{"timestamp": "2026-01-01"}],
    }
    entry = cache.lookup("1", "youtrack", "abc123", "read_full")
    assert entry is not None
    assert entry.from_cache is True
    assert entry.content == "contenido cacheado"


def test_lookup_cache_miss(cache, mock_collection):
    """Cuando ChromaDB retorna lista vacía, lookup() debe retornar None (cache miss)."""
    mock_collection.get.return_value = {"documents": [], "metadatas": []}
    entry = cache.lookup("1", "youtrack", "abc123", "read_full")
    assert entry is None


def test_store_calls_upsert(cache, mock_collection):
    """store() debe llamar a ChromaDB.upsert() con el documento y metadatos correctos."""
    entry = CacheEntry(
        item_id="1",
        provider_name="youtrack",
        content_hash="abc",
        tool="read_full",
        content="test",
        metadata={"a": 1},
        from_cache=False,
    )
    cache.store(entry)
    mock_collection.upsert.assert_called_once()
    call_args = mock_collection.upsert.call_args
    assert call_args.kwargs["documents"] == ["test"]


def test_invalidate_calls_delete(cache, mock_collection):
    """invalidate() llama a ChromaDB.delete() con item_id, provider_name y tool."""
    cache.invalidate("1", "youtrack", "read_full")
    mock_collection.delete.assert_called_once_with(
        where={"item_id": "1", "provider_name": "youtrack", "tool": "read_full"}
    )
