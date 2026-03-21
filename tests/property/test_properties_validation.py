# Feature: contextforge, Propiedad 1: Validación de campos faltantes en ProviderConfig
# Feature: contextforge, Propiedad 19: Validación de providers vacío en SessionConfig

from hypothesis import given, settings
from hypothesis import strategies as st

from app.session import SessionManager
from settings import Settings
from src.domain.entities import LLMConfig, ProviderConfig, SessionConfig
from src.domain.exceptions import SessionConfigError


class TestSessionManagerValidation:
    @given(
        token=st.one_of(st.just(""), st.just("   "), st.just("\t")),
        base_url=st.one_of(st.none(), st.text(min_size=0, max_size=200)),
    )
    @settings(max_examples=100)
    def test_empty_token_raises_error(self, token: str, base_url: str | None) -> None:
        config = SessionConfig(
            providers={"test": ProviderConfig(code="youtrack", token=token, base_url=base_url)}
        )
        manager = SessionManager()
        try:
            manager.store("session-1", config)
            assert False, "Expected SessionConfigError"
        except SessionConfigError as e:
            assert "token" in str(e).lower()

    def test_empty_providers_raises_error(self) -> None:
        config = SessionConfig(providers={})
        manager = SessionManager()
        try:
            manager.store("session-1", config)
            assert False, "Expected SessionConfigError"
        except SessionConfigError as e:
            assert "proveedor" in str(e).lower()

    @given(
        token=st.text(min_size=1, max_size=100).filter(lambda s: s.strip() != ""),
        base_url=st.one_of(st.none(), st.text(min_size=0, max_size=200)),
    )
    @settings(max_examples=100)
    def test_valid_config_stored_successfully(self, token: str, base_url: str | None) -> None:
        config = SessionConfig(
            providers={"youtrack": ProviderConfig(code="youtrack", token=token, base_url=base_url)}
        )
        manager = SessionManager()
        manager.store("session-1", config)
        retrieved = manager.get("session-1")
        assert retrieved.providers["youtrack"].token == token

    def test_get_nonexistent_session_raises_error(self) -> None:
        manager = SessionManager()
        try:
            manager.get("nonexistent")
            assert False, "Expected SessionConfigError"
        except SessionConfigError as e:
            assert "no encontrada" in str(e).lower()

    def test_delete_nonexistent_session_is_silent(self) -> None:
        manager = SessionManager()
        manager.delete("nonexistent")
        assert "nonexistent" not in manager._sessions


class TestSettingsValidation:
    @given(api_key=st.one_of(st.just(""), st.just("  "), st.just("\n\t")))
    @settings(max_examples=50)
    def test_empty_llm_api_key_raises_error(self, api_key: str) -> None:
        settings = Settings(llm_api_key=api_key, _env_file=None)
        try:
            settings.get_llm_config()
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "LLM_API_KEY" in str(e)

    def test_valid_llm_config_returned(self) -> None:
        settings = Settings(llm_api_key="test-key-123", _env_file=None)
        config = settings.get_llm_config()
        assert isinstance(config, LLMConfig)
        assert config.api_key == "test-key-123"
        assert config.engine_type == "gemini"

    def test_default_values(self) -> None:
        # We use _env_file=None to ensure we testing the defaults in the class, not the local .env
        settings = Settings(llm_api_key="valid-key", _env_file=None)
        assert settings.llm_engine == "gemini"
        assert settings.llm_model_version == "gemini-2.5-flash-lite"
        assert settings.chroma_host == "chromadb"
        assert settings.chroma_port == 8000
        assert settings.mcp_port == 3000
