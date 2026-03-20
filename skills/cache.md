---
inclusion: manual
---

# Skill: Cache

Repositorio de caché usando ChromaDB.

## Archivo

```
src/infrastructure/cache/
└── chroma.py    # ChromaCacheRepository
```

## ChromaCacheRepository

```python
class ChromaCacheRepository(CacheRepositoryInterface):
    def __init__(self, host: str, port: int):
        self._client = chromadb.HttpClient(host=host, port=port)
        self._collection = self._client.get_or_create_collection("contextforge_cache")

    def lookup(self, item_id, provider_name, content_hash, tool, **kwargs) -> CacheEntry | None:
        # Filtra por: item_id + provider_name + content_hash + tool
        # + max_tokens si está en kwargs
        ...

    def store(self, entry: CacheEntry) -> None:
        doc_id = f"{entry.item_id}::{entry.provider_name}::{entry.content_hash}::{entry.tool}"
        # upsert con documentos y metadatos

    def invalidate(self, item_id, provider_name, tool) -> None:
        self._collection.delete(where={...})
```

## Clave de Caché

Compuesta por: `item_id + provider_name + content_hash + tool`

Para `read_summarize`: + `max_tokens`
Para `read_chunks`: + `chunk_index`

## Flujo Híbrido

1. Ir al proveedor → obtener `content_hash`
2. Buscar en caché por `content_hash`
3. Si hit → retornar caché
4. Si miss → procesar, guardar, retornar

## Convenciones

- Colección: `contextforge_cache`
- Host/puerto configurables
- Filtro por metadatos (no similitud semántica)

## Referencia

Ver `.kiro/specs/contextforge/design.md` sección ChromaDB.
