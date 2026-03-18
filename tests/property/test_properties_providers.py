from hypothesis import given, settings
from hypothesis import strategies as st

from src.infrastructure.builders.context_item import ContextItemBuilder


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
