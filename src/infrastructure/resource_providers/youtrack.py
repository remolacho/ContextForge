import re
from urllib.parse import urlparse

from src.domain.interfaces import ResourceResolverInterface


class YouTrackResourceResolver(ResourceResolverInterface):
    _URL_PATTERN = re.compile(r"https?://[^/]+/issue/([A-Z]+-\d+)", re.IGNORECASE)

    def resolve(self, resource: str) -> str:
        if not resource:
            raise ValueError("Resource no puede estar vacío")

        resource = resource.strip()

        if self._is_youtrack_url(resource):
            return self._extract_id_from_url(resource)

        return resource

    def _is_youtrack_url(self, resource: str) -> bool:
        try:
            parsed = urlparse(resource)
            return bool(parsed.scheme and parsed.netloc and "issue" in resource.lower())
        except Exception:
            return False

    def _extract_id_from_url(self, url: str) -> str:
        match = self._URL_PATTERN.search(url)
        if not match:
            raise ValueError(f"No se pudo extraer ID de YouTrack de la URL: {url}")
        return match.group(1)
