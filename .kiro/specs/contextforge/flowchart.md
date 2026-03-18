# ContextForge - Diagrama de Flujo

## Flujo Híbrido (Cache-First con Datos Frescos)

```mermaid
flowchart TD
    A[Agente MCP] -->|tool_call| B{MCP Controller}
    
    B -->|read_full| C[ReadFullUseCase]
    B -->|read_summarize| D[ReadSummarizeUseCase]
    B -->|read_chunks| E[ReadChunksUseCase]
    
    subgraph "Paso 1: Obtener contenido fresco"
        C --> C1[provider.get_item<br/>item_id]
        D --> D1[provider.get_item<br/>item_id]
        E --> E1[provider.get_item<br/>item_id]
    end
    
    C1 --> C2[ContextItemBuilder<br/>build → raw_content<br/>content_hash]
    D1 --> D2[ContextItemBuilder<br/>build → raw_content<br/>content_hash]
    E1 --> E2[ContextItemBuilder<br/>build → raw_content<br/>content_hash]
    
    subgraph "Paso 2: Buscar en caché"
        C2 --> C3[cache.lookup<br/>item_id + provider<br/>content_hash + tool<br/>+ params]
        D2 --> D3[cache.lookup<br/>item_id + provider<br/>content_hash + tool<br/>max_tokens]
        E2 --> E3[cache.lookup<br/>item_id + provider<br/>content_hash + tool<br/>chunk_index]
    end
    
    C3 --> C4{¿Cache Hit?}
    D3 --> D4{¿Cache Hit?}
    E3 --> E4{¿Cache Hit?}
    
    C4 -->|Sí| C5[Retornar<br/>CacheEntry<br/>from_cache=True]
    D4 -->|Sí| D5[Retornar<br/>CacheEntry<br/>from_cache=True]
    E4 -->|Sí| E5[Retornar<br/>Chunks<br/>from_cache=True]
    
    C4 -->|No| C6[tool: read_full<br/>content = raw_content]
    D4 -->|No| D6[llm.summarize<br/>raw_content<br/>max_tokens]
    E4 -->|No| E6[_split_into_chunks<br/>raw_content<br/>≤500 tokens]
    
    subgraph "Paso 3: Guardar en caché"
        C6 --> C7[CacheEntryBuilder<br/>for_item + tool<br/>+ content]
        D6 --> D7[CacheEntryBuilder<br/>for_item + tool<br/>+ summary<br/>+ max_tokens]
        E6 --> E7[Para cada chunk<br/>CacheEntryBuilder<br/>+ chunk_index]
    end
    
    C7 --> C8[cache.store]
    D7 --> D8[cache.store]
    E7 --> E8[cache.store]
    
    C8 --> C5
    D8 --> D5
    E8 --> E5
    
    C5 --> Z[Respuesta al<br/>Agente MCP]
    D5 --> Z
    E5 --> Z
```

---

## Arquitectura de Capas

```mermaid
flowchart TB
    subgraph "Interface Layer"
        MCP[main.py<br/>FastAPI + MCP]
        CTRL[MCP Controller]
        SCH[Pydantic Schemas]
        SESSION[Session Manager]
    end
    
    subgraph "Application Layer"
        SVC[ContextService<br/>Facade]
        UC1[ReadFullUseCase]
        UC2[ReadSummarizeUseCase]
        UC3[ReadChunksUseCase]
    end
    
    subgraph "Domain Layer"
        ENT[Entities<br/>ContextItem<br/>CacheEntry<br/>Chunk]
        IF[Interfaces<br/>ProviderInterface<br/>CacheRepositoryInterface<br/>LLMEngineInterface]
        EX[Exceptions]
    end
    
    subgraph "Infrastructure Layer"
        PF[ProviderFactory]
        YT[YouTrackProvider]
        JIRA[JiraProvider]
        CH[ChromaCache]
        LLM[GeminiLLMEngine]
        CIB[ContextItemBuilder]
        CEB[CacheEntryBuilder]
    end
    
    MCP --> CTRL
    CTRL --> SVC
    SVC --> UC1
    SVC --> UC2
    SVC --> UC3
    
    UC1 --> IF
    UC2 --> IF
    UC3 --> IF
    
    IF --> ENT
    IF --> EX
    
    UC1 --> PF
    UC2 --> PF
    UC3 --> PF
    
    PF --> YT
    PF --> JIRA
    
    UC2 --> LLM
    UC3 --> LLM
    
    UC1 --> CH
    UC2 --> CH
    UC3 --> CH
    
    YT --> CIB
    JIRA --> CIB
    CIB --> CEB
    CEB --> CH
```

---

## Cache Lookup - Claves

```mermaid
flowchart LR
    subgraph "Cache Key Structure"
        K1[item_id]
        K2[provider_name]
        K3[content_hash]
        K4[tool]
        K5[params<br/>max_tokens<br/>chunk_index]
    end
    
    K1 --> K01[&bull;]
    K2 --> K01
    K3 --> K01
    K4 --> K01
    K5 --> K01
    
    K01 -->|Unique ID| DOC[ChromaDB<br/>Document + Metadata]
    
    style K01 fill:#90EE90,stroke:#333
    style DOC fill:#87CEEB,stroke:#333
```

---

## Estados de Cache

```mermaid
stateDiagram-v2
    [*] --> Proveedor
    Proveedor --> CacheLookup: get content_hash
    
    state CacheLookup {
        [*] --> QueryChroma
        QueryChroma --> Hit:Encontrado
        QueryChroma --> Miss:No encontrado
    }
    
    Hit --> RetornarCache: from_cache=True
    Miss --> EjecutarTool
    EjecutarTool --> GuardarCache: store(entry)
    GuardarCache --> RetornarNuevo: from_cache=False
    
    RetornarCache --> [*]
    RetornarNuevo --> [*]
```

---

## Detección de Cambios

```mermaid
flowchart TD
    A[Item en Proveedor<br/>cambia] --> B[Nueva solicitud<br/>del agente]
    
    B --> C[provider.get_item<br/>item_id]
    C --> D[Calcula<br/>content_hash_nuevo]
    
    D --> E[cache.lookup<br/>content_hash_novo]
    
    E --> F{¿Encontrado?}
    
    F -->|Sí| G[Retornar<br/>cache]
    F -->|No| H[content_hash cambió<br/>→ Cache MISS]
    
    H --> I[Ejecutar tool]
    I --> J[Guardar nuevo<br/>en cache]
    J --> K[Retornar<br/>resultado]
    
    G --> L[El contenido<br/>no cambió<br/>→ Optimizado]
    K --> L
    
    style H fill:#FFB6C1,stroke:#333
    style L fill:#90EE90,stroke:#333
```

---

## Diferencias entre Tools

| Tool | Cache Key | Contenido Cacheado | Params Extra |
|------|-----------|-------------------|--------------|
| `read_full` | item_id + provider + content_hash + tool | raw_content | - |
| `read_summarize` | ... + tool + max_tokens | summary | max_tokens |
| `read_chunks` | ... + tool + chunk_index | chunk content | chunk_index |

---

## Ejemplo: Read Summarize Flow

```mermaid
sequenceDiagram
    participant Agente
    participant MCP as MCP Controller
    participant UC as ReadSummarizeUseCase
    participant Prov as YouTrackProvider
    participant LLM as GeminiLLMEngine
    participant Cache as ChromaDB

    Agente->>MCP: tools/call<br/>read_summarize("PROJ-123", max_tokens=500)
    MCP->>UC: execute("PROJ-123", "youtrack", max_tokens=500)
    
    Note over UC: Flujo Híbrido
    
    UC->>Prov: get_item("PROJ-123")
    Prov-->>UC: ContextItem<br/>raw_content<br/>content_hash=abc123
    
    UC->>Cache: lookup(item_id, provider, content_hash=abc123, tool=read_summarize, max_tokens=500)
    
    alt Cache Hit
        Cache-->>UC: CacheEntry(summary)
        UC-->>MCP: CacheEntry(from_cache=True)
    else Cache Miss
        UC->>LLM: summarize(raw_content, max_tokens=500)
        LLM-->>UC: summary text
        
        UC->>Cache: store(CacheEntry)
        UC-->>MCP: CacheEntry(from_cache=False)
    end
    
    MCP-->>Agente: {content: summary, from_cache: bool}
```
