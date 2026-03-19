from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.domain.exceptions import LLMError
from src.domain.interfaces import LLMEngineInterface, SummarizeEngineInterface


class Summarized(SummarizeEngineInterface):
    def __init__(
        self,
        engine_llm: LLMEngineInterface,
        prompt_template: ChatPromptTemplate,
    ) -> None:
        self._llm = engine_llm.llm
        self._embeddings = engine_llm.embeddings
        self._chain = prompt_template | self._llm | StrOutputParser()

    def summarize(self, content: str, max_tokens: int) -> str:
        try:
            return self._chain.invoke(
                {
                    "content": content,
                    "max_tokens": max_tokens,
                }
            )
        except Exception as e:
            raise LLMError(f"Error al generar resumen: {e}") from e

    def count_tokens(self, text: str) -> int:
        return self._llm.get_num_tokens(text)

    def get_embeddings(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)
