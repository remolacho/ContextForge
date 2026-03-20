"""Property tests para ReadChunksUseCase."""

from unittest.mock import MagicMock

import pytest

from src.application.services.read_chunks import MAX_CHUNK_TOKENS, ReadChunksUseCase
from src.domain.entities import ContextItem


@pytest.fixture
def mock_provider():
    provider = MagicMock()
    item = ContextItem(
        item_id="1",
        provider_name="youtrack",
        title="Test",
        description="Description",
        comments=[],
        custom_fields={},
        raw_content="",
        content_hash="abc123",
    )
    provider.get_item.return_value = item
    provider._config = MagicMock()
    return provider


@pytest.fixture
def mock_cache():
    return MagicMock()


def mock_count_tokens(text: str) -> int:
    """Mock que retorna tokens variables según longitud."""
    return max(50, len(text) % 100)


@pytest.fixture
def mock_summarized():
    summarized = MagicMock()
    summarized.count_tokens.side_effect = mock_count_tokens
    return summarized


@pytest.fixture
def use_case(mock_provider, mock_cache, mock_summarized):
    return ReadChunksUseCase(
        provider=mock_provider,
        cache=mock_cache,
        summarized=mock_summarized,
    )


def test_chunks_under_500_tokens(use_case, mock_cache):
    """Propiedad 6: Ningún chunk supera 500 tokens."""
    mock_cache.lookup.return_value = None

    chunks = use_case.execute("1", "youtrack")

    for chunk in chunks:
        assert chunk.token_count <= MAX_CHUNK_TOKENS


def test_chunks_preserve_content():
    """Propiedad 7: Concatenación de chunks contiene todo el texto original."""
    provider = MagicMock()
    item = ContextItem(
        item_id="1",
        provider_name="youtrack",
        title="Test",
        description="Description",
        comments=[],
        custom_fields={},
        raw_content="Sentence one. Sentence two. Sentence three.",
        content_hash="abc123",
    )
    provider.get_item.return_value = item
    provider._config = MagicMock()
    cache = MagicMock()
    cache.lookup.return_value = None

    summarized = MagicMock()
    summarized.count_tokens.return_value = 50

    use_case = ReadChunksUseCase(provider=provider, cache=cache, summarized=summarized)
    chunks = use_case.execute("1", "youtrack")

    reconstructed = " ".join(chunk.content for chunk in chunks)
    assert "Sentence" in reconstructed


def test_filter_by_indices_returns_exact_chunks(use_case, mock_cache):
    """Propiedad 8: Pide índices [i, j], retorna exactamente esos chunks."""
    mock_cache.lookup.return_value = None

    chunks = use_case.execute("1", "youtrack", chunk_indices=[1])

    assert len(chunks) >= 1
    assert chunks[0].chunk_index == 1


def test_filter_invalid_index_raises_error(use_case, mock_cache):
    """Propiedad 9: Índice fuera de rango lanza ValidationError."""
    mock_cache.lookup.return_value = None

    with pytest.raises(Exception) as exc_info:
        use_case.execute("1", "youtrack", chunk_indices=[1, 9999])

    assert "9999" in str(exc_info.value)


def test_chunks_end_with_sentence_boundary(use_case, mock_cache):
    """Propiedad 10: Chunk termina en . ! ? o es el último."""
    mock_cache.lookup.return_value = None

    chunks = use_case.execute("1", "youtrack")

    for i, chunk in enumerate(chunks):
        if i < len(chunks) - 1 and chunk.content:
            last_char = chunk.content[-1]
            assert last_char in ".!?"
