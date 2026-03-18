from src.domain.entities import LLMConfig
from src.domain.exceptions import LLMEngineNotRegisteredError
from src.domain.interfaces import LLMEngineInterface
from src.infrastructure.llm.gemini import GeminiLLMEngine


class LLMFactory:
    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def create(self) -> LLMEngineInterface:
        engine_type = self.config.engine_type
        if engine_type == "gemini":
            return GeminiLLMEngine(self.config)
        raise LLMEngineNotRegisteredError(
            f"Motor LLM '{engine_type}' no reconocido. Disponibles: gemini"
        )
