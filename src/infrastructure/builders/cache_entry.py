from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from src.domain.entities import CacheEntry, ContextItem

if TYPE_CHECKING:
    from src.domain.entities import ContextItem


@dataclass
class CacheEntryBuilder:
    _item_id: Optional[str] = field(default=None)
    _provider_name: Optional[str] = field(default=None)
    _content_hash: Optional[str] = field(default=None)
    _tool: Optional[str] = field(default=None)
    _content: str = field(default="")
    _metadata: dict = field(default_factory=dict)

    def for_item(self, item: "ContextItem") -> "CacheEntryBuilder":
        self._item_id = item.item_id
        self._provider_name = item.provider_name
        self._content_hash = item.content_hash
        return self

    def with_tool(self, tool: str) -> "CacheEntryBuilder":
        self._tool = tool
        return self

    def with_content(self, content: str) -> "CacheEntryBuilder":
        self._content = content
        return self

    def with_metadata(self, **kwargs) -> "CacheEntryBuilder":
        self._metadata.update(kwargs)
        return self

    def build(self) -> CacheEntry:
        if self._item_id is None:
            raise ValueError("item_id is required")
        if self._provider_name is None:
            raise ValueError("provider_name is required")
        if self._content_hash is None:
            raise ValueError("content_hash is required")
        if self._tool is None:
            raise ValueError("tool is required")

        return CacheEntry(
            item_id=self._item_id,
            provider_name=self._provider_name,
            content_hash=self._content_hash,
            tool=self._tool,
            content=self._content,
            metadata=self._metadata,
            from_cache=False,
        )
