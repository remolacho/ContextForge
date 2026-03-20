"""Punto de entrada del servidor ContextForge MCP."""

from fastapi import FastAPI

from app.exceptions.exception_handler import exception_handlers
from app.session import SessionManager
from config.routes import Routes
from settings import get_settings
from src.application.services.context_service import ContextService
from src.infrastructure.cache.chroma import ChromaCacheRepository
from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.tools.summarizer.summarize import Summarized
from src.infrastructure.tools.summarizer.summarizer_engine import Summarizer
from src.infrastructure.tools.tokenizer import TiktokenTokenizer

settings = get_settings()

cache = ChromaCacheRepository(host=settings.chroma_host, port=settings.chroma_port)

llm_engine = LLMFactory(settings.get_llm_config()).create()

summarizer = Summarizer(llm=llm_engine.llm, tokenizer=TiktokenTokenizer())
summarized = Summarized(engine_llm=llm_engine, summarizer=summarizer)

context_service = ContextService(
    cache=cache,
    summarized=summarized,
    tokenizer=TiktokenTokenizer(),
)
session_manager = SessionManager()

app = FastAPI(
    title="ContextForge MCP Server",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

for exc_class, handler in exception_handlers.items():
    app.add_exception_handler(exc_class, handler)

Routes(app, context_service=context_service, session_manager=session_manager).register()
