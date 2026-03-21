"""Summarizer: responsable del proceso map-reduce."""

from langchain_core.output_parsers import StrOutputParser

from src.domain.exceptions import LLMError
from src.domain.interfaces import TokenizerInterface
from src.infrastructure.templates_prompts.summarize_map import SUMMARIZE_MAP_PROMPT
from src.infrastructure.templates_prompts.summarize_reduce import SUMMARIZE_REDUCE_PROMPT


class Summarizer:
    def __init__(self, llm, tokenizer: TokenizerInterface, chunk_size: int = 500):
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        self._llm = llm
        self._tokenizer = tokenizer
        self._chunk_size = chunk_size
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            # LangChain llama internamente: length_function(texto) → int
            length_function=tokenizer.count_tokens,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    # ════════ ZONA PÚBLICA ════════

    def summarize(self, content: str, max_tokens: int) -> str:
        chunks = self._splitter.split_text(content)
        if len(chunks) == 1:
            return self._summarize_single(chunks[0], max_tokens)
        return self._map_reduce(chunks, max_tokens)

    # ════════ ZONA PRIVADA ════════

    def _summarize_single(self, content: str, max_tokens: int) -> str:
        return self._invoke(SUMMARIZE_MAP_PROMPT, content, max_tokens)

    def _map_reduce(self, chunks: list[str], max_tokens: int) -> str:
        partial = [self._summarize_single(c, max_tokens // len(chunks)) for c in chunks]
        combined = "\n\n".join(partial)
        return self._invoke(SUMMARIZE_REDUCE_PROMPT, combined, max_tokens)

    def _invoke(self, prompt, content: str, max_tokens: int) -> str:
        try:
            formatted = prompt.invoke({"content": content, "max_tokens": max_tokens})
            return StrOutputParser().invoke(self._llm.invoke(formatted))
        except Exception as e:
            raise LLMError(f"Error al generar resumen: {e}") from e
