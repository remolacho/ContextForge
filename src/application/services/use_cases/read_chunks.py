"""ReadChunksUseCase: Divide contenido en chunks usando RecursiveCharacterTextSplitter."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.domain.entities import CacheEntry, Chunk
from src.domain.exceptions import ValidationError
from src.domain.interfaces import (
    CacheRepositoryInterface,
    ProviderInterface,
    TokenizerInterface,
)
from src.infrastructure.builders.cache_entry import CacheEntryBuilder

MAX_CHUNK_TOKENS = 500


class ReadChunksUseCase:
    """Divide texto en chunks y los guarda en caché."""

    def __init__(
        self,
        provider: ProviderInterface,
        cache: CacheRepositoryInterface,
        tokenizer: TokenizerInterface,
    ) -> None:
        self._provider = provider
        self._cache = cache
        self._tokenizer = tokenizer
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHUNK_TOKENS,
            length_function=tokenizer.count_tokens,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def execute(
        self,
        item_id: str,
        provider_name: str,
        chunk_indices: list[int] | None = None,
    ) -> list[Chunk]:
        """Retorna chunks del item, desde caché o generados."""
        item = self._provider.get_item(item_id, self._provider._config)  # type: ignore[attr-defined]
        chunks = self._get_or_generate_chunks(item, provider_name)
        if chunk_indices is not None:
            return self._filter_by_indices(chunks, chunk_indices)
        return chunks

    def _get_or_generate_chunks(self, item, provider_name: str) -> list[Chunk]:
        """Obtiene de caché o genera chunks."""
        cached = self._cache.lookup(item.item_id, provider_name, item.content_hash, "read_chunks")
        if cached:
            return self._deserialize_chunks(cached)
        return self._create_and_cache_chunks(item, provider_name)

    def _create_and_cache_chunks(self, item, provider_name: str) -> list[Chunk]:
        """Genera chunks y los guarda en caché."""
        texts = self._splitter.split_text(item.raw_content)
        chunks = [
            Chunk(
                chunk_index=i + 1,
                total_chunks=len(texts),
                content=text,
                token_count=self._tokenizer.count_tokens(text),
            )
            for i, text in enumerate(texts)
        ]
        for chunk in chunks:
            self._store_chunk(item, chunk)
        return chunks

    def _store_chunk(self, item, chunk: Chunk) -> None:
        """Guarda un chunk individual en caché."""
        entry = (
            CacheEntryBuilder()
            .for_item(item)
            .with_tool("read_chunks")
            .with_content(chunk.content)
            .with_metadata(chunk_index=chunk.chunk_index, total_chunks=chunk.total_chunks)
            .build()
        )
        self._cache.store(entry)

    def _deserialize_chunks(self, cached: CacheEntry) -> list[Chunk]:
        """Recupera chunks desde caché."""
        return []

    def _filter_by_indices(self, chunks: list[Chunk], indices: list[int]) -> list[Chunk]:
        """Filtra chunks por índices solicitados."""
        self._validate_indices(chunks, indices)
        return [c for c in chunks if c.chunk_index in indices]

    def _validate_indices(self, chunks: list[Chunk], indices: list[int]) -> None:
        """Lanza error si algún índice es inválido."""
        total = len(chunks)
        for idx in indices:
            if not (1 <= idx <= total):
                raise ValidationError(f"chunk_index {idx} inválido. Índices válidos: 1 a {total}")
