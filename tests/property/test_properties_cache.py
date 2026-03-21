# Feature: contextforge, Propiedad 3: Round-trip de caché por herramienta
# Feature: contextforge, Propiedad 11: Cache miss cuando content_hash cambia

from unittest.mock import MagicMock, patch

from hypothesis import given, settings
from hypothesis import strategies as st

from src.domain.entities import CacheEntry
from src.infrastructure.cache.chroma import ChromaCacheRepository


class TestCacheRoundTrip:
    def setup_method(self) -> None:
        self.mock_collection = MagicMock()
        self.mock_client = MagicMock()
        self.mock_client.get_or_create_collection.return_value = self.mock_collection

    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_lookup_returns_same_content_with_from_cache_true(
        self,
        mock_http_client: MagicMock,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        item_id = "MCF-123"
        provider_name = "youtrack"
        content_hash = "abc123"
        tool = "read_full"
        content = "Full content of the item"

        self.mock_collection.get.return_value = {
            "documents": [content],
            "metadatas": [{"item_id": item_id, "provider_name": provider_name}],
        }

        result = repo.lookup(item_id, provider_name, content_hash, tool)

        assert result is not None
        assert result.content == content
        assert result.from_cache is True
        assert result.item_id == item_id
        assert result.provider_name == provider_name

    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_round_trip_for_different_tools(
        self,
        mock_http_client: MagicMock,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        tools = ["read_full", "read_summarize", "read_chunks"]

        for tool in tools:
            item_id = f"MCF-{tool}"
            content_hash = f"hash_{tool}"
            content = f"Content for {tool}"

            self.mock_collection.get.return_value = {
                "documents": [content],
                "metadatas": [{"tool": tool}],
            }

            result = repo.lookup(item_id, "youtrack", content_hash, tool)

            assert result is not None
            assert result.content == content
            assert result.from_cache is True
            assert result.tool == tool

    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_round_trip_with_max_tokens_for_summarize(
        self,
        mock_http_client: MagicMock,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        item_id = "MCF-456"
        content_hash = "hash_summary"
        content = "Summarized content"
        max_tokens = 500

        self.mock_collection.get.return_value = {
            "documents": [content],
            "metadatas": [{"tool": "read_summarize", "max_tokens": max_tokens}],
        }

        result = repo.lookup(
            item_id,
            "youtrack",
            content_hash,
            "read_summarize",
            max_tokens=max_tokens,
        )

        assert result is not None
        assert result.content == content
        assert result.from_cache is True

    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_store_and_lookup_round_trip(
        self,
        mock_http_client: MagicMock,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        entry = CacheEntry(
            item_id="MCF-789",
            provider_name="youtrack",
            content_hash="stored_hash",
            tool="read_full",
            content="Stored content",
            metadata={},
            from_cache=False,
        )

        stored_content = "Stored content"

        def mock_get(where, include):
            if where.get("content_hash") == entry.content_hash:
                return {
                    "documents": [stored_content],
                    "metadatas": [
                        {
                            "item_id": entry.item_id,
                            "provider_name": entry.provider_name,
                            "content_hash": entry.content_hash,
                            "tool": entry.tool,
                        }
                    ],
                }
            return {"documents": [], "metadatas": []}

        self.mock_collection.get.side_effect = mock_get

        repo.store(entry)

        self.mock_collection.upsert.assert_called_once()

        result = repo.lookup(
            entry.item_id,
            entry.provider_name,
            entry.content_hash,
            entry.tool,
        )

        assert result is not None
        assert result.from_cache is True


class TestCacheInvalidation:
    def setup_method(self) -> None:
        self.mock_collection = MagicMock()
        self.mock_client = MagicMock()
        self.mock_client.get_or_create_collection.return_value = self.mock_collection

    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_cache_miss_when_hash_changes(
        self,
        mock_http_client: MagicMock,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        item_id = "MCF-123"
        provider_name = "youtrack"
        new_hash = "new_hash_xyz"
        tool = "read_full"

        self.mock_collection.get.return_value = {"documents": [], "metadatas": []}

        result = repo.lookup(item_id, provider_name, new_hash, tool)

        assert result is None

    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_cache_hit_when_hash_same(
        self,
        mock_http_client: MagicMock,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        item_id = "MCF-123"
        provider_name = "youtrack"
        content_hash = "stable_hash_123"
        tool = "read_full"
        cached_content = "Cached content"

        def mock_get(where, include):
            if where.get("content_hash") == content_hash:
                return {
                    "documents": [cached_content],
                    "metadatas": [{"content_hash": content_hash}],
                }
            return {"documents": [], "metadatas": []}

        self.mock_collection.get.side_effect = mock_get

        result = repo.lookup(item_id, provider_name, content_hash, tool)

        assert result is not None
        assert result.from_cache is True
        assert result.content == cached_content

    @given(
        item_id=st.text(min_size=1, max_size=50),
        provider_name=st.one_of(st.just("youtrack"), st.just("jira")),
        tool=st.one_of(
            st.just("read_full"),
            st.just("read_summarize"),
            st.just("read_chunks"),
        ),
    )
    @settings(max_examples=100)
    @patch("src.infrastructure.cache.chroma.chromadb.HttpClient")
    def test_different_hash_always_misses(
        self,
        mock_http_client: MagicMock,
        item_id: str,
        provider_name: str,
        tool: str,
    ) -> None:
        mock_http_client.return_value = self.mock_client
        repo = ChromaCacheRepository(host="localhost", port=8000)

        self.mock_collection.get.return_value = {"documents": [], "metadatas": []}

        result = repo.lookup(item_id, provider_name, "different_hash", tool)

        assert result is None


class TestCacheProperties:
    @given(
        item_id=st.text(min_size=1, max_size=50),
        provider_name=st.text(min_size=1, max_size=50),
        content_hash=st.text(min_size=1, max_size=64),
        tool=st.sampled_from(["read_full", "read_summarize", "read_chunks"]),
    )
    @settings(max_examples=50)
    def test_lookup_returns_consistent_results(
        self,
        item_id: str,
        provider_name: str,
        content_hash: str,
        tool: str,
    ) -> None:
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        content = f"Content for {item_id} from {provider_name}"

        def mock_get(where, include):
            if where.get("content_hash") == content_hash:
                return {
                    "documents": [content],
                    "metadatas": [
                        {
                            "item_id": item_id,
                            "provider_name": provider_name,
                            "tool": tool,
                        }
                    ],
                }
            return {"documents": [], "metadatas": []}

        mock_collection.get.side_effect = mock_get

        with patch(
            "src.infrastructure.cache.chroma.chromadb.HttpClient",
            return_value=mock_client,
        ):
            repo = ChromaCacheRepository(host="localhost", port=8000)

            result1 = repo.lookup(item_id, provider_name, content_hash, tool)
            result2 = repo.lookup(item_id, provider_name, content_hash, tool)

            assert result1 is not None
            assert result2 is not None
            assert result1.content == result2.content
            assert result1.from_cache is True
            assert result2.from_cache is True

    @given(
        item_id=st.text(min_size=1, max_size=50),
        provider_name=st.text(min_size=1, max_size=50),
        content_hash=st.text(min_size=1, max_size=64),
        tool=st.sampled_from(["read_full", "read_summarize", "read_chunks"]),
        content=st.text(min_size=1, max_size=1000),
    )
    @settings(max_examples=50)
    def test_cache_roundtrip_property(
        self,
        item_id: str,
        provider_name: str,
        content_hash: str,
        tool: str,
        content: str,
    ) -> None:
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        def mock_get(where, include):
            if (
                where.get("item_id") == item_id
                and where.get("provider_name") == provider_name
                and where.get("content_hash") == content_hash
                and where.get("tool") == tool
            ):
                return {
                    "documents": [content],
                    "metadatas": [
                        {
                            "item_id": item_id,
                            "provider_name": provider_name,
                            "content_hash": content_hash,
                            "tool": tool,
                        }
                    ],
                }
            return {"documents": [], "metadatas": []}

        mock_collection.get.side_effect = mock_get

        with patch(
            "src.infrastructure.cache.chroma.chromadb.HttpClient",
            return_value=mock_client,
        ):
            repo = ChromaCacheRepository(host="localhost", port=8000)

            entry = CacheEntry(
                item_id=item_id,
                provider_name=provider_name,
                content_hash=content_hash,
                tool=tool,
                content=content,
                metadata={},
                from_cache=False,
            )

            repo.store(entry)
            result = repo.lookup(item_id, provider_name, content_hash, tool)

            assert result is not None
            assert result.content == content
            assert result.from_cache is True
            assert result.item_id == item_id
            assert result.provider_name == provider_name
            assert result.content_hash == content_hash
            assert result.tool == tool
