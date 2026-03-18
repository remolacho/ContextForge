from dataclasses import dataclass
from typing import Optional


@dataclass
class ProviderConfig:
    code: str                     # "youtrack", "jira" - identifica el proveedor
    token: str
    base_url: Optional[str] = None


@dataclass
class SessionConfig:
    providers: dict[str, ProviderConfig]


@dataclass
class LLMConfig:
    engine_type: str
    api_key: str


@dataclass
class ContextItem:
    item_id: str
    provider_name: str
    title: str
    description: str
    comments: list[str]
    custom_fields: dict
    raw_content: str
    content_hash: str


@dataclass
class Chunk:
    chunk_index: int
    total_chunks: int
    content: str
    token_count: int


@dataclass
class CacheEntry:
    item_id: str
    provider_name: str
    content_hash: str
    tool: str
    content: str
    metadata: dict
    from_cache: bool = False
