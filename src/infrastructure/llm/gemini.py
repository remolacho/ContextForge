from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src.domain.entities import LLMConfig
from src.domain.interfaces import LLMEngineInterface


class GeminiLLMEngine(LLMEngineInterface):
    def __init__(self, config: LLMConfig) -> None:
        self._config = config
        self._llm = ChatGoogleGenerativeAI(
            model=config.model_version,
            google_api_key=config.api_key,
        )
        self._embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=config.api_key,
        )  # type: ignore[call-arg]

    @property
    def llm(self) -> ChatGoogleGenerativeAI:
        return self._llm

    @property
    def embeddings(self) -> GoogleGenerativeAIEmbeddings:
        return self._embeddings
