from langchain_core.prompts import ChatPromptTemplate

SUMMARIZE_MAP_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente técnico especializado en resumir contenido.\n\n"
            "Reglas:\n"
            "- Máximo {max_tokens} tokens\n"
            "- Incluir puntos clave y relevantes\n"
            "- Mantener claridad y precisión\n"
            "- No inventar información",
        ),
        ("human", "Fragmento a resumir:\n\n{content}"),
    ]
)
