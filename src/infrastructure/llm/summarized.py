from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.domain.exceptions import LLMError
from src.domain.interfaces import LLMEngineInterface, TextProcessingInterface


class Summarized(TextProcessingInterface):
    def __init__(
        self,
        engine_llm: LLMEngineInterface,
        prompt_template: ChatPromptTemplate,
    ) -> None:
        self._llm = engine_llm.llm
        self._embeddings = engine_llm.embeddings
        self._prompt_template = prompt_template

    def summarize(self, content: str, max_tokens: int) -> str:
        try:
            formatted_prompt = self._prompt_template.invoke(
                {
                    "content": content,
                    "max_tokens": max_tokens,
                }
            )
            llm_response = self._llm.invoke(formatted_prompt)
            return StrOutputParser().invoke(llm_response)
        except Exception as e:
            raise LLMError(f"Error al generar resumen: {e}") from e

    def count_tokens(self, text: str) -> int:
        return self._llm.get_num_tokens(text)

    def get_embeddings(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)
