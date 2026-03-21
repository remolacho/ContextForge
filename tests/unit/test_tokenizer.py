from src.infrastructure.tools.tokenizer import TiktokenTokenizer


def test_count_tokens_returns_correct_count():
    tokenizer = TiktokenTokenizer()
    tokens = tokenizer.count_tokens("Hello, world!")
    assert tokens > 0


def test_fallback_to_cl100k_base():
    tokenizer = TiktokenTokenizer(encoding_name="unknown-model")
    tokens = tokenizer.count_tokens("test")
    assert tokens > 0
