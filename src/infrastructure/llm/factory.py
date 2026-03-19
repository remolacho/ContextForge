from src.domain.entities import LLMConfig
from src.domain.exceptions import LLMEngineNotRegisteredError
from src.domain.interfaces import SummarizeEngineInterface
from src.infrastructure.llm.gemini import GeminiLLMEngine
from src.infrastructure.llm.prompts import SUMMARIZE_PROMPT
from src.infrastructure.llm.summarized import Summarized


class LLMFactory:
    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def create(self) -> SummarizeEngineInterface:
        engine_type = self.config.engine_type
        if engine_type == "gemini":
            engine_llm = GeminiLLMEngine(self.config)
            return Summarized(engine_llm, SUMMARIZE_PROMPT)
        raise LLMEngineNotRegisteredError(
            f"Motor LLM '{engine_type}' no reconocido. Disponibles: gemini"
        )
