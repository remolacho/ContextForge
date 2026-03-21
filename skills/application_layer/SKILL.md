# Application Layer (ContextService and Use Cases)

The Application Layer orchestrates the interaction between the Interface Layer and the Domain/Infrastructure layers.

## 1. ContextService (Facade Pattern)
The `ContextService` acts as a facade, providing a simplified interface for the Interface Layer to call various business functionalities without worrying about complex implementation details. It delegates implementation to specific handle-based use cases.

## 2. Use Cases
The business logic is divided into specialized use cases, each following the **Single Responsibility Principle**:
- **`ReadFullUseCase`**: Retrieves the entire detailed content of an item (e.g., ticket) from a provider.
- **`ReadSummarizeUseCase`**: Uses an LLM to generate a condensed version (summary) of a specific item, effectively optimizing token counts for AI agents.
- **`ReadChunksUseCase`**: Segments extended content into smaller fragments (chunks) of up to 500 tokens each to facilitate fine-grained navigation.

## 3. Interaction Flow
The Application Layer receives a `SessionConfig` and parameters from the Interface Layer's handlers. It then orchestrates various infrastructure ports (e.g., `ProviderInterface`, `CacheRepositoryInterface`, `LLMEngineInterface`) to retrieve, process, cache, and deliver the final domain objects to the Interface Layer.
