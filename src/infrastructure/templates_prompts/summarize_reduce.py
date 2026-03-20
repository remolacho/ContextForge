from langchain_core.prompts import ChatPromptTemplate

SUMMARIZE_REDUCE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente técnico especializado en sintetizar información.\n\n"
            "Reglas:\n"
            "- Máximo {max_tokens} tokens\n"
            "- Crear resumen coherente de los fragmentos\n"
            "- Eliminar redundancias\n"
            "- Mantener estructura lógica\n"
            "- No inventar información",
        ),
        ("human", "Resúmenes parciales a combinar:\n\n{combined}"),
    ]
)
