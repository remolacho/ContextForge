# Domain Layer (Entities, Ports, and Exceptions)

The Domain Layer defines the core business model and abstractions, representing the internal state and operation of the application. It is the most internal layer in the Clean Architecture.

## 1. Core Domain Entities
Entities represent the business objects used throughout the application:
- **`ContextItem`**: Represents a specific item retrieved from a provider (e.g., ticket data).
- **`Chunk`**: Represents a fragment of a larger `ContextItem`.
- **`CacheEntry`**: Represents a cached entry with its metadata.
- **`ProviderConfig`, `SessionConfig`, `LLMConfig`**: Represent the configuration and state of the current session and its providers.

## 2. Ports (Interfaces)
The Domain Layer defines the interfaces that outer layers must implement, applying the **Dependency Inversion Principle**:
- **`ProviderInterface`**: Interface for multi-provider task retrieval (e.g., YouTrack, Jira).
- **`CacheRepositoryInterface`**: Interface for persistent storage (e.g., ChromaDB).
- **`LLMEngineInterface`**: Interface for LLM-based text processing and summarization.
- **`TextProcessingInterface`**: Interface for additional text transformations.

## 3. Domain Exceptions
A comprehensive hierarchy of business-related errors (`ContextForgeError`, `SessionConfigError`, `ItemNotFoundError`, etc.) provides precise error propagation that is eventually handled by the Interface Layer's global exception handlers.
