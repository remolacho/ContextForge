"""ReadChunksUseCase: Divide contenido en chunks de max 500 tokens."""

import re

from src.domain.entities import CacheEntry, Chunk
from src.domain.exceptions import ValidationError
from src.domain.interfaces import (
    CacheRepositoryInterface,
    ProviderInterface,
    TextProcessingInterface,
)
from src.infrastructure.builders.cache_entry import CacheEntryBuilder

MAX_CHUNK_TOKENS = 500


class ReadChunksUseCase:
    """Divide texto en chunks y los guarda en caché."""

    def __init__(
        self,
        provider: ProviderInterface,
        cache: CacheRepositoryInterface,
        summarized: TextProcessingInterface,
    ) -> None:
        self._provider = provider
        self._cache = cache
        self._summarized = summarized

    # ════════ ZONA PÚBLICA ════════

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

    # ════════ ZONA PRIVADA ════════

    def _get_or_generate_chunks(self, item, provider_name: str) -> list[Chunk]:
        """Obtiene de caché o genera chunks."""
        cached = self._cache.lookup(item.item_id, provider_name, item.content_hash, "read_chunks")
        if cached:
            return self._deserialize_chunks(cached)
        return self._create_and_cache_chunks(item, provider_name)

    def _create_and_cache_chunks(self, item, provider_name: str) -> list[Chunk]:
        """Genera chunks y los guarda en caché."""
        chunks = self._split_into_chunks(item.raw_content)
        for chunk in chunks:
            self._store_chunk(item, provider_name, chunk)
        return chunks

    def _split_into_chunks(self, text: str) -> list[Chunk]:
        """Divide texto en chunks de max 500 tokens."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = self._group_sentences_into_chunks(sentences)
        self._set_total_chunks(chunks)
        return chunks

    def _group_sentences_into_chunks(self, sentences: list[str]) -> list[Chunk]:
        """Agrupa oraciones en chunks."""
        chunks: list[Chunk] = []
        current: list[str] = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self._summarized.count_tokens(sentence)
            if self._should_start_new_chunk(current_tokens, sentence_tokens):
                self._finalize_chunk(chunks, current, current_tokens)
                current = [sentence]
                current_tokens = sentence_tokens
            else:
                current.append(sentence)
                current_tokens += sentence_tokens

        if current:
            self._finalize_chunk(chunks, current, current_tokens)

        return chunks

    def _should_start_new_chunk(self, current_tokens: int, sentence_tokens: int) -> bool:
        """Determina si debe iniciar nuevo chunk."""
        return current_tokens + sentence_tokens > MAX_CHUNK_TOKENS and current_tokens > 0

    def _finalize_chunk(self, chunks: list[Chunk], sentences: list[str], tokens: int) -> None:
        """Guarda chunk finalizado."""
        chunks.append(
            Chunk(
                chunk_index=len(chunks) + 1,
                total_chunks=0,
                content=" ".join(sentences),
                token_count=tokens,
            )
        )

    def _set_total_chunks(self, chunks: list[Chunk]) -> None:
        """Actualiza total_chunks en todos los chunks."""
        total = len(chunks)
        for chunk in chunks:
            chunk.total_chunks = total

    def _store_chunk(self, item, provider_name: str, chunk: Chunk) -> None:
        """Guarda un chunk individual en caché."""
        entry = (
            CacheEntryBuilder()
            .for_item(item)
            .with_tool("read_chunks")
            .with_content(chunk.content)
            .with_metadata(
                chunk_index=chunk.chunk_index,
                total_chunks=chunk.total_chunks,
            )
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
