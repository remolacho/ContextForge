"""Tests para ContextService."""

from unittest.mock import MagicMock

import pytest

from src.application.services.context_service import ContextService
from src.domain.entities import ProviderConfig, SessionConfig
from src.domain.exceptions import SessionConfigError
from src.domain.interfaces import (
    CacheRepositoryInterface,
    TextProcessingInterface,
    TokenizerInterface,
)


@pytest.fixture
def mock_cache() -> MagicMock:
    return MagicMock(spec=CacheRepositoryInterface)


@pytest.fixture
def mock_summarized() -> MagicMock:
    return MagicMock(spec=TextProcessingInterface)


@pytest.fixture
def mock_tokenizer() -> MagicMock:
    return MagicMock(spec=TokenizerInterface)


@pytest.fixture
def session_config() -> SessionConfig:
    return SessionConfig(
        providers={
            "youtrack": ProviderConfig(
                code="youtrack",
                token="test_token",
                base_url="https://test.youtrack.cloud",
            )
        }
    )


@pytest.fixture
def service(
    mock_cache: MagicMock,
    mock_summarized: MagicMock,
    mock_tokenizer: MagicMock,
) -> ContextService:
    return ContextService(
        cache=mock_cache,
        summarized=mock_summarized,
        tokenizer=mock_tokenizer,
    )


class TestContextServiceValidation:
    def test_read_full_raises_error_for_unknown_provider(
        self,
        service: ContextService,
        session_config: SessionConfig,
    ) -> None:
        with pytest.raises(SessionConfigError) as exc_info:
            service.read_full(item_id="TEST-1", provider_name="unknown", session=session_config)
        assert "Proveedor 'unknown' no configurado" in str(exc_info.value)
        assert "youtrack" in str(exc_info.value)

    def test_read_summarize_raises_error_for_unknown_provider(
        self,
        service: ContextService,
        session_config: SessionConfig,
    ) -> None:
        with pytest.raises(SessionConfigError) as exc_info:
            service.read_summarize(
                item_id="TEST-1", provider_name="unknown", session=session_config
            )
        assert "Proveedor 'unknown' no configurado" in str(exc_info.value)

    def test_read_chunks_raises_error_for_unknown_provider(
        self,
        service: ContextService,
        session_config: SessionConfig,
    ) -> None:
        with pytest.raises(SessionConfigError) as exc_info:
            service.read_chunks(item_id="TEST-1", provider_name="unknown", session=session_config)
        assert "Proveedor 'unknown' no configurado" in str(exc_info.value)

    def test_error_includes_available_providers(
        self,
        service: ContextService,
        session_config: SessionConfig,
    ) -> None:
        with pytest.raises(SessionConfigError) as exc_info:
            service.read_full(item_id="TEST-1", provider_name="jira", session=session_config)
        assert "jira" in str(exc_info.value)
        assert "youtrack" in str(exc_info.value)
