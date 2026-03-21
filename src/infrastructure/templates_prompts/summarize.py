from langchain_core.prompts import ChatPromptTemplate

SUMMARIZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente técnico especializado en resumir contenido de manera "
            "concisa y precisa.\n\n"
            "Reglas:\n"
            "- Máximo {max_tokens} tokens\n"
            "- Incluir solo información relevante y verificable\n"
            "- Mantener claridad y estructura\n"
            "- No inventar ni añadir información no presente en el contenido original\n"
            "- Priorizar: problema, contexto, estado actual, puntos clave",
        ),
        (
            "human",
            "Contenido a resumir:\n\n{content}",
        ),
    ]
)
