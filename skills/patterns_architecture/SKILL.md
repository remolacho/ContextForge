# Architecture and Design Patterns

This skill describes the high-level architecture and design patterns used in the ContextForge project.

## 1. High-Level Architecture
ContextForge follows **Clean Architecture** principles combined with **SOLID** design patterns. The codebase is organized into four concentric layers, ensuring that dependencies always point inward towards the Domain Layer.

- **Interface Layer**: FastAPI controllers, handlers, schemas, and entry point.
- **Application Layer**: Application services (Facade) and use cases.
- **Domain Layer**: Core business logic, entities, ports (interfaces), and exceptions.
- **Infrastructure Layer**: Concrete implementations of ports (providers, cache, LLM, builders, factories).

## 2. SOLID Principles Application
- **S (Single Responsibility)**: Each component has a unique responsibility (e.g., use cases, controllers).
- **O (Open/Closed)**: dynamic registration in `ProviderFactory` and `LLMFactory` allows adding new implementations without modifying existing code.
- **L (Liskov Substitution)**: All providers implement `ProviderInterface`, making them interchangeable.
- **I (Interface Segregation)**: Granular interfaces for providers, cache, and LLM functionality.
- **D (Dependency Inversion)**: High-level modules (use cases) depend on abstractions (interfaces), not low-level implementations (infrastructure).

## 3. Design Patterns
- **Factory**: Used in `ProviderFactory` and `LLMFactory` for dynamic instantiation of providers and LLM engines.
- **Facade**: `ContextService` acts as a facade between the Interface Layer and the Use Cases in the Application Layer.
- **Builder**: `ContextItemBuilder` and `CacheEntryBuilder` facilitate the creation of complex domain entities from provider-specific data.
- **Strategy**: Handlers in the interface layer and individual providers implementation use this pattern to switch between different execution modes.
- **Repository**: `CacheRepositoryInterface` abstracts persistent storage operations (ChromaDB), decoupling business logic from storage.
