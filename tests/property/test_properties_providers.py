from hypothesis import given, settings
from hypothesis import strategies as st

from src.domain.entities import LLMConfig, ProviderConfig
from src.domain.exceptions import LLMEngineNotRegisteredError, ProviderNotRegisteredError
from src.infrastructure.builders.context_item import ContextItemBuilder
from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.llm.summarized import Summarized
from src.infrastructure.providers.factory import ProviderFactory
from src.infrastructure.providers.task.youtrack import YouTrackProvider


@given(
    title=st.text(),
    description=st.text(),
    comments=st.lists(st.text()),
)
@settings(max_examples=100)
def test_context_item_builder_deterministic_hash(title: str, description: str, comments: list[str]):
    """Propiedad 20: ContextItemBuilder produce content_hash SHA-256 consistente"""
    builder1 = (
        ContextItemBuilder()
        .set_item_id("123")
        .set_provider_name("youtrack")
        .set_title(title)
        .set_description(description)
        .set_comments(comments)
        .build()
    )

    builder2 = (
        ContextItemBuilder()
        .set_item_id("123")
        .set_provider_name("youtrack")
        .set_title(title)
        .set_description(description)
        .set_comments(comments)
        .build()
    )

    assert builder1.content_hash == builder2.content_hash


@given(
    title=st.text(),
    description=st.text(),
    comments=st.lists(st.text()),
)
@settings(max_examples=100)
def test_context_item_builder_different_content_different_hash(
    title: str, description: str, comments: list[str]
):
    """Propiedad 20: Contenido diferente produce hash diferente"""
    builder = (
        ContextItemBuilder()
        .set_item_id("123")
        .set_provider_name("youtrack")
        .set_title(title)
        .set_description(description)
        .set_comments(comments)
        .build()
    )

    if title or description or comments:
        builder_modified = (
            ContextItemBuilder()
            .set_item_id("123")
            .set_provider_name("youtrack")
            .set_title(title + " modified")
            .set_description(description)
            .set_comments(comments)
            .build()
        )

        assert builder.content_hash != builder_modified.content_hash


# Feature: contextforge, Propiedad 16: ProviderFactory crea segun config.code


def test_provider_factory_creates_youtrack():
    """Propiedad 16: ProviderFactory crea YouTrackProvider para code='youtrack'"""
    config = ProviderConfig(code="youtrack", token="test")
    factory = ProviderFactory(config)
    provider = factory.create()
    assert isinstance(provider, YouTrackProvider)


def test_provider_factory_unknown_code():
    """Propiedad 16: Code desconocido lanza ProviderNotRegisteredError"""
    config = ProviderConfig(code="unknown", token="test")
    factory = ProviderFactory(config)
    try:
        factory.create()
        assert False, "Should have raised ProviderNotRegisteredError"
    except ProviderNotRegisteredError as e:
        assert "unknown" in str(e)


# Feature: contextforge, Propiedad 18: LLMFactory crea segun LLMConfig.engine_type


def test_llm_factory_creates_gemini():
    """Propiedad 18: LLMFactory crea Summarized para engine_type='gemini'"""
    config = LLMConfig(engine_type="gemini", api_key="test")
    factory = LLMFactory(config)
    engine = factory.create()
    assert isinstance(engine, Summarized)


def test_llm_factory_unknown_engine():
    """Propiedad 18: Engine desconocido lanza LLMEngineNotRegisteredError"""
    config = LLMConfig(engine_type="unknown", api_key="test")
    factory = LLMFactory(config)
    try:
        factory.create()
        assert False, "Should have raised LLMEngineNotRegisteredError"
    except LLMEngineNotRegisteredError as e:
        assert "unknown" in str(e)
