from langchain_core.prompts import ChatPromptTemplate

SUMMARIZE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """Eres un asistente técnico especializado en resumir contenido de manera concisa y precisa.

Reglas:
- Máximo {max_tokens} tokens
- Incluir solo información relevante y verificable
- Mantener claridad y estructura
- No inventar ni añadir información no presente en el contenido original
- Priorizar: problema, contexto, estado actual, puntos clave""",
    ),
    (
        "human",
        "Contenido a resumir:\n\n{content}",
    ),
])
