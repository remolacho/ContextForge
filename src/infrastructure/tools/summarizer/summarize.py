from src.domain.interfaces import LLMEngineInterface, TextProcessingInterface


class Summarized(TextProcessingInterface):
    def __init__(self, engine_llm: LLMEngineInterface, summarizer):
        self._llm = engine_llm.llm
        self._embeddings = engine_llm.embeddings
        self._summarizer = summarizer

    # ════════ ZONA PÚBLICA ════════

    def summarize(self, content: str, max_tokens: int) -> str:
        return self._summarizer.summarize(content, max_tokens)

    def count_tokens(self, text: str) -> int:
        return self._llm.get_num_tokens(text)

    def get_embeddings(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)
