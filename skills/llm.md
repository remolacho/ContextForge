---
inclusion: manual
---

# Skill: LLM

Motor LLM y procesamiento de texto.

## Archivos

```
src/infrastructure/llm/
├── factory.py      # LLMFactory
├── gemini.py       # GeminiLLMEngine

src/infrastructure/tools/
├── tokenizer.py    # TiktokenTokenizer
└── summarizer/
    ├── summarize.py          # Summarized
    └── summarizer_engine.py  # MapReduce
```

## LLMFactory

```python
class LLMFactory:
    def create(self) -> LLMEngineInterface:
        if self.config.engine_type == "gemini":
            return GeminiLLMEngine(self.config)
        raise LLMEngineNotRegisteredError(...)
```

## GeminiLLMEngine

```python
class GeminiLLMEngine(LLMEngineInterface):
    def __init__(self, config: LLMConfig):
        self._llm = ChatGoogleGenerativeAI(model=config.model_version, ...)
        self._embeddings = GoogleGenerativeAIEmbeddings(...)

    @property
    def llm(self) -> ChatGoogleGenerativeAI: ...

    @property
    def embeddings(self) -> GoogleGenerativeAIEmbeddings: ...
```

## TiktokenTokenizer

```python
class TiktokenTokenizer(TokenizerInterface):
    def count_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))
```

## Summarized (TextProcessingInterface)

```python
class Summarized(TextProcessingInterface):
    def summarize(self, content: str, max_tokens: int) -> str: ...
    def count_tokens(self, text: str) -> int: ...
    def get_embeddings(self, text: str) -> list[float]: ...
```

## Summarizer (MapReduce)

Para textos largos:
1. Split en chunks
2. Map: resumir cada chunk
3. Reduce: combinar resúmenes

## Convenciones

- Usar LangChain LCEL para chains
- tiktoken para conteo de tokens
- Encoding: `cl100k_base` (default)

## Referencia

Ver `.kiro/specs/contextforge/design.md` sección LLM.
