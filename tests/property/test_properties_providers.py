from hypothesis import given, settings
from hypothesis import strategies as st

from src.domain.entities import ProviderConfig
from src.domain.exceptions import ProviderNotRegisteredError
from src.infrastructure.builders.context_item import ContextItemBuilder
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
