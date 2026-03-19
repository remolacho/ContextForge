from src.domain.entities import LLMConfig
from src.domain.exceptions import LLMEngineNotRegisteredError
from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.llm.gemini import GeminiLLMEngine
from src.infrastructure.llm.prompts import SUMMARIZE_PROMPT
from src.infrastructure.llm.summarized import Summarized


def test_llm_factory_creates_gemini():
    """Propiedad 18: LLMFactory crea GeminiLLMEngine para engine_type='gemini'"""
    config = LLMConfig(engine_type="gemini", api_key="test")
    factory = LLMFactory(config)
    engine = factory.create()
    assert isinstance(engine, GeminiLLMEngine)


def test_llm_factory_creates_summarized():
    """Propiedad 18: Summarized recibe GeminiLLMEngine y template para summarization"""
    config = LLMConfig(engine_type="gemini", api_key="test")
    factory = LLMFactory(config)
    engine = factory.create()
    summarized = Summarized(engine, SUMMARIZE_PROMPT)
    assert isinstance(summarized, Summarized)


def test_llm_factory_unknown_engine():
    """Propiedad 18: Engine desconocido lanza LLMEngineNotRegisteredError"""
    config = LLMConfig(engine_type="unknown", api_key="test")
    factory = LLMFactory(config)
    try:
        factory.create()
        assert False, "Should have raised LLMEngineNotRegisteredError"
    except LLMEngineNotRegisteredError as e:
        assert "unknown" in str(e)
