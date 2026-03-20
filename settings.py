"""Configuración del servidor via variables de entorno."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.domain.entities import LLMConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    llm_engine: str = "gemini"
    llm_api_key: str = ""
    llm_model_version: str = "gemini-2.5-flash-lite"

    chroma_host: str = "chromadb"
    chroma_port: int = 8000

    mcp_port: int = 3000

    def get_llm_config(self) -> LLMConfig:
        if not self.llm_api_key or not self.llm_api_key.strip():
            raise ValueError("LLM_API_KEY is required")
        return LLMConfig(
            engine_type=self.llm_engine,
            api_key=self.llm_api_key,
            model_version=self.llm_model_version,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
