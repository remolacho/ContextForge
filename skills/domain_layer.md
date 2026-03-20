---
inclusion: manual
---

# Skill: Domain Layer

Define entidades, interfaces y excepciones del dominio.

## Archivos

```
src/domain/
├── entities.py      # dataclasses
├── interfaces.py    # ABCs
└── exceptions.py    # excepciones
```

## Entidades

```python
@dataclass
class ProviderConfig:
    code: str
    token: str
    base_url: str | None = None

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
```

## Interfaces (Ports)

| Interface | Métodos |
|-----------|---------|
| `ProviderInterface` | `get_item()`, `validate_config()` |
| `CacheRepositoryInterface` | `lookup()`, `store()`, `invalidate()` |
| `LLMEngineInterface` | `.llm`, `.embeddings` (properties) |
| `TextProcessingInterface` | `summarize()`, `count_tokens()`, `get_embeddings()` |
| `TokenizerInterface` | `count_tokens()` |

## Excepciones

Jerarquía bajo `ContextForgeError`:

| Excepción | HTTP |
|-----------|------|
| `ConfigurationError` | - |
| `SessionConfigError` | 400 |
| `AuthenticationError` | 401 |
| `ItemNotFoundError` | 404 |
| `ProviderServerError` | 5xx |
| `CacheError` | - |
| `LLMError` | - |
| `ValidationError` | 422 |
| `ProviderNotRegisteredError` | 422 |
| `LLMEngineNotRegisteredError` | 422 |

## Convenciones

- Entidades: `@dataclass` de Python
- Interfaces: ABC con `@abstractmethod`
- Excepciones: heredan de `ContextForgeError`
- Sin dependencias externas

## Referencia

Ver `.kiro/specs/contextforge/design.md` para detalles completos.
