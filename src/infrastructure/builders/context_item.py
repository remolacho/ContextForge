import hashlib
from dataclasses import dataclass, field
from typing import Optional

from src.domain.entities import ContextItem


@dataclass
class ContextItemBuilder:
    _item_id: Optional[str] = field(default=None)
    _provider_name: Optional[str] = field(default=None)
    _title: Optional[str] = field(default=None)
    _description: Optional[str] = field(default=None)
    _comments: list[str] = field(default_factory=list)
    _custom_fields: dict = field(default_factory=dict)

    def set_item_id(self, item_id: str) -> "ContextItemBuilder":
        self._item_id = item_id
        return self

    def set_provider_name(self, name: str) -> "ContextItemBuilder":
        self._provider_name = name
        return self

    def set_title(self, title: str) -> "ContextItemBuilder":
        self._title = title
        return self

    def set_description(self, description: str) -> "ContextItemBuilder":
        self._description = description
        return self

    def set_comments(self, comments: list[str]) -> "ContextItemBuilder":
        self._comments = comments
        return self

    def set_custom_fields(self, custom_fields: dict) -> "ContextItemBuilder":
        self._custom_fields = custom_fields
        return self

    def build(self) -> ContextItem:
        if self._item_id is None:
            raise ValueError("item_id is required")
        if self._provider_name is None:
            raise ValueError("provider_name is required")

        raw_content = self._title or ""
        if self._description:
            raw_content += f"\n{self._description}"
        for comment in self._comments:
            raw_content += f"\n{comment}"

        content_hash = hashlib.sha256(raw_content.encode()).hexdigest()

        return ContextItem(
            item_id=self._item_id,
            provider_name=self._provider_name,
            title=self._title or "",
            description=self._description or "",
            comments=self._comments,
            custom_fields=self._custom_fields,
            raw_content=raw_content,
            content_hash=content_hash,
        )
