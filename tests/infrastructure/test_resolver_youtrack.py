import pytest

from src.domain.exceptions import ResourceResolverNotRegisteredError
from src.infrastructure.resource_providers import ResourceResolverFactory, YouTrackResourceResolver


@pytest.fixture
def resolver():
    return YouTrackResourceResolver()


@pytest.fixture
def factory():
    return ResourceResolverFactory()


class TestYouTrackResourceResolver:
    def test_resolve_with_id(self, resolver):
        """Cuando se pasa un ID directo, debe retornarlo sin cambios."""
        assert resolver.resolve("MCF-24") == "MCF-24"

    def test_resolve_with_full_url(self, resolver):
        """Cuando se pasa una URL completa de YouTrack, debe extraer el ID."""
        url = "https://communities.youtrack.cloud/issue/MCF-24"
        assert resolver.resolve(url) == "MCF-24"

    def test_resolve_with_url_trailing_slash(self, resolver):
        """Debe funcionar con URLs que terminan en slash."""
        url = "https://communities.youtrack.cloud/issue/MCF-24/"
        assert resolver.resolve(url) == "MCF-24"

    def test_resolve_with_url_trailing_text(self, resolver):
        """Debe funcionar con URLs que tienen texto adicional."""
        url = "https://communities.youtrack.cloud/issue/MCF-24?constructor=1"
        assert resolver.resolve(url) == "MCF-24"

    def test_resolve_with_stripped_whitespace(self, resolver):
        """Debe eliminar espacios en blanco alrededor del resource."""
        assert resolver.resolve("  MCF-24  ") == "MCF-24"

    def test_resolve_empty_raises_error(self, resolver):
        """Cuando el resource está vacío, debe lanzar ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            resolver.resolve("")

    def test_resolve_invalid_url_returns_as_is(self, resolver):
        """Cuando la URL no tiene patrón de YouTrack, debe retornarla tal cual."""
        assert resolver.resolve("https://example.com/task/123") == "https://example.com/task/123"

    def test_resolve_http_url(self, resolver):
        """Debe funcionar con URLs HTTP (no solo HTTPS)."""
        url = "http://communities.youtrack.cloud/issue/MCF-24"
        assert resolver.resolve(url) == "MCF-24"


class TestResourceResolverFactory:
    def test_factory_creates_youtrack(self, factory):
        """Factory debe crear YouTrackResourceResolver para provider 'youtrack'."""
        resolver = factory.create("youtrack")
        assert isinstance(resolver, YouTrackResourceResolver)

    def test_factory_creates_youtrack_case_insensitive(self, factory):
        """Factory debe crear resolver sin importar el case del provider."""
        resolver = factory.create("YouTrack")
        assert isinstance(resolver, YouTrackResourceResolver)

    def test_factory_unknown_provider_raises_error(self, factory):
        """Cuando el provider no está registrado, debe lanzar ResourceResolverNotRegisteredError."""
        with pytest.raises(ResourceResolverNotRegisteredError) as exc_info:
            factory.create("github")
        assert "github" in str(exc_info.value)
