from app.session import SessionManager
from src.application.services.context_service import ContextService
from src.domain.entities import CacheEntry, Chunk, SessionConfig
from src.infrastructure.resource_providers import ResourceResolverFactory


class ToolCallHandler:
    def __init__(self, context_service: ContextService, session_manager: SessionManager) -> None:
        self._context_service = context_service
        self._session_manager = session_manager
        self._resolver_factory = ResourceResolverFactory()

    def execute(
        self,
        tool_name: str,
        arguments: dict,
        session: SessionConfig,
    ) -> CacheEntry | list[Chunk]:
        resource = arguments.get("resource", "")
        provider_name = arguments.get("provider_name", "")

        resolver = self._resolver_factory.create(provider_name)
        item_id = resolver.resolve(resource)

        if tool_name == "read_full":
            return self._context_service.read_full(item_id, provider_name, session)

        if tool_name == "read_summarize":
            max_tokens = arguments.get("max_tokens", 500)
            return self._context_service.read_summarize(item_id, provider_name, session, max_tokens)

        if tool_name == "read_chunks":
            chunk_indices = arguments.get("chunk_indices")
            return self._context_service.read_chunks(item_id, provider_name, session, chunk_indices)

        raise ValueError(f"Herramienta '{tool_name}' no soportada")
