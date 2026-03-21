from src.domain.entities import LLMConfig
from src.domain.exceptions import LLMEngineNotRegisteredError
from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.llm.gemini import GeminiLLMEngine
from src.infrastructure.tools.summarizer import Summarized, Summarizer
from src.infrastructure.tools.tokenizer import TiktokenTokenizer


def test_llm_factory_creates_gemini():
    """Propiedad 18: LLMFactory crea GeminiLLMEngine para engine_type='gemini'"""
    config = LLMConfig(engine_type="gemini", api_key="test")
    factory = LLMFactory(config)
    engine = factory.create()
    assert isinstance(engine, GeminiLLMEngine)


def test_llm_factory_creates_summarized():
    """Propiedad 18: Summarized recibe Summarizer para map-reduce"""
    config = LLMConfig(engine_type="gemini", api_key="test")
    factory = LLMFactory(config)
    engine = factory.create()
    tokenizer = TiktokenTokenizer()
    summarizer = Summarizer(engine.llm, tokenizer)
    summarized = Summarized(engine, summarizer)
    assert isinstance(summarized, Summarized)


def test_summarizer_initialization():
    """Summarizer se inicializa con llm, tokenizer y chunk_size"""
    config = LLMConfig(engine_type="gemini", api_key="test")
    factory = LLMFactory(config)
    engine = factory.create()
    tokenizer = TiktokenTokenizer()
    summarizer = Summarizer(engine.llm, tokenizer, chunk_size=500)
    assert summarizer._chunk_size == 500


def test_llm_factory_unknown_engine():
    """Propiedad 18: Engine desconocido lanza LLMEngineNotRegisteredError"""
    config = LLMConfig(engine_type="unknown", api_key="test")
    factory = LLMFactory(config)
    try:
        factory.create()
        assert False, "Should have raised LLMEngineNotRegisteredError"
    except LLMEngineNotRegisteredError as e:
        assert "unknown" in str(e)
