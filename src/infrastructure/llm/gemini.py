from src.domain.entities import LLMConfig
from src.domain.interfaces import LLMEngineInterface


class GeminiLLMEngine(LLMEngineInterface):
    def __init__(self, config: LLMConfig) -> None:
        self._config = config

    def summarize(self, content: str, max_tokens: int) -> str:
        raise NotImplementedError("GeminiLLMEngine no implementado aún")

    def count_tokens(self, text: str) -> int:
        raise NotImplementedError("GeminiLLMEngine no implementado aún")

    def get_embeddings(self, text: str) -> list[float]:
        raise NotImplementedError("GeminiLLMEngine no implementado aún")
