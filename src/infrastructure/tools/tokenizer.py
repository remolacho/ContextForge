import tiktoken

from src.domain.interfaces import TokenizerInterface


class TiktokenTokenizer(TokenizerInterface):
    def __init__(self, encoding_name: str = "cl100k_base") -> None:
        self._encoding = self._get_encoding(encoding_name)

    @staticmethod
    def _get_encoding(model: str) -> tiktoken.Encoding:
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            return tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))
