---
inclusion: manual
---

# Skill: Builders

Patrón Builder para construir objetos complejos.

## Archivos

```
src/infrastructure/builders/
├── context_item.py   # ContextItemBuilder
└── cache_entry.py    # CacheEntryBuilder
```

## ContextItemBuilder

Construye `ContextItem` desde campos genéricos.

```python
class ContextItemBuilder:
    def set_item_id(self, item_id: str) -> "ContextItemBuilder": ...
    def set_provider_name(self, name: str) -> "ContextItemBuilder": ...
    def set_title(self, title: str) -> "ContextItemBuilder": ...
    def set_description(self, description: str) -> "ContextItemBuilder": ...
    def set_comments(self, comments: list[str]) -> "ContextItemBuilder": ...
    def set_custom_fields(self, custom_fields: dict) -> "ContextItemBuilder": ...
    def build(self) -> ContextItem:  # calcula raw_content y content_hash
```

**Importante:** El builder es agnóstico al proveedor. Cada proveedor transforma su JSON específico a campos genéricos antes de pasarlos.

## CacheEntryBuilder

Construye `CacheEntry` con todos sus metadatos.

```python
class CacheEntryBuilder:
    def for_item(self, item: ContextItem) -> "CacheEntryBuilder": ...
    def with_tool(self, tool: str) -> "CacheEntryBuilder": ...
    def with_content(self, content: str) -> "CacheEntryBuilder": ...
    def with_metadata(self, **kwargs) -> "CacheEntryBuilder": ...
    def build(self) -> CacheEntry:
```

## Convenciones

- Métodos fluidos (retornan `self`)
- Métodos encadenables
- `build()` calcula campos derivados automáticamente
- `content_hash` = SHA-256 de `raw_content`

## Referencia

Ver `.kiro/specs/contextforge/design.md` sección Builders.
