from src.domain.exceptions import ResourceResolverNotRegisteredError
from src.domain.interfaces import ResourceResolverInterface
from src.infrastructure.resource_providers.youtrack import YouTrackResourceResolver


class ResourceResolverFactory:
    def create(self, provider_name: str) -> ResourceResolverInterface:
        if provider_name.lower() == "youtrack":
            return YouTrackResourceResolver()

        raise ResourceResolverNotRegisteredError(
            f"Provider '{provider_name}' no reconocido. Disponibles: youtrack"
        )
