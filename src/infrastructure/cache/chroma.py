import chromadb

from ...domain.entities import CacheEntry
from ...domain.interfaces import CacheRepositoryInterface


class ChromaCacheRepository(CacheRepositoryInterface):
    def __init__(self, host: str, port: int) -> None:
        self._client = chromadb.HttpClient(host=host, port=port)
        self._collection = self._client.get_or_create_collection("contextforge_cache")

    def lookup(
        self,
        item_id: str,
        provider_name: str,
        content_hash: str,
        tool: str,
        **kwargs,
    ) -> CacheEntry | None:
        where = {
            "item_id": item_id,
            "provider_name": provider_name,
            "content_hash": content_hash,
            "tool": tool,
        }
        if "max_tokens" in kwargs:
            where["max_tokens"] = kwargs["max_tokens"]
        results = self._collection.get(where=where, include=["documents", "metadatas"])  # type: ignore[arg-type]
        if not results["documents"]:
            return None
        metadata = results["metadatas"][0] if results["metadatas"] else {}
        return CacheEntry(
            item_id=item_id,
            provider_name=provider_name,
            content_hash=content_hash,
            tool=tool,
            content=results["documents"][0],
            metadata=metadata,  # type: ignore[arg-type]
            from_cache=True,
        )

    def store(self, entry: CacheEntry) -> None:
        doc_id = _build_doc_id(entry)
        self._collection.upsert(
            ids=[doc_id],
            documents=[entry.content],
            metadatas=[
                {
                    **entry.metadata,
                    "item_id": entry.item_id,
                    "provider_name": entry.provider_name,
                    "content_hash": entry.content_hash,
                    "tool": entry.tool,
                }
            ],
        )

    def invalidate(self, item_id: str, provider_name: str, tool: str) -> None:
        self._collection.delete(
            where={"item_id": item_id, "provider_name": provider_name, "tool": tool}  # type: ignore[arg-type]
        )


def _build_doc_id(entry: CacheEntry) -> str:
    base = f"{entry.item_id}::{entry.provider_name}::{entry.content_hash}::{entry.tool}"
    if entry.tool == "read_summarize" and "max_tokens" in entry.metadata:
        return f"{base}::{entry.metadata['max_tokens']}"
    if entry.tool == "read_chunks" and "chunk_index" in entry.metadata:
        return f"{base}::{entry.metadata['chunk_index']}"
    return base
