# Infrastructure Layer (Concrete Implementations)

The Infrastructure Layer contains the concrete implementations of the interfaces defined in the Domain Layer.

## 1. Providers (Task Retrieval)
- **`ProviderFactory`**: Manages the dynamic instantiation and registration of various providers.
- **`YouTrackProvider`**: A functional implementation for retrieving ticket data from YouTrack.
- **Future Stubs**: Placeholders for `GitHubProvider`, `GitLabProvider`, etc., which will implement `ProviderInterface`.

## 2. LLM Engine (Summarization)
- **`LLMFactory`**: Handles the instantiation and configuration of LLM engines (e.g., Gemini).
- **`GeminiLLMEngine`**: A concrete implementation using LangChain and Google's Generative AI to perform summarization (Map-Reduce/Chain setup).
- **`Summarized (TextProcessingInterface)`**: A specialized component for text transformations and summarization.

## 3. Persistent Storage (Caching)
- **`ChromaCacheRepository`**: An implementation of `CacheRepositoryInterface` that utilizes **ChromaDB** for vector-based or simple text caching with persistent storage (local Docker volume).

## 4. Builders and Tooling
- **`ContextItemBuilder`**: Transforms provider-specific JSON data into high-level Domain `ContextItem` entities.
- **`CacheEntryBuilder`**: Efficiently creates `CacheEntry` domain entities from processed content.
- **`TiktokenTokenizer`**: Provides precise token counting for AI agents to meet token constraints.
