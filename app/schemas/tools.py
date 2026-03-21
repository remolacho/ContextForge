TOOLS_DEFINITION = [
    {
        "name": "read_full",
        "description": "Recupera la totalidad del contenido de un ítem (ticket, issue, etc.) "
        "de un proveedor configurado. Úsalo cuando el usuario necesite el detalle completo "
        "sin omisiones.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource": {
                    "type": "string",
                    "description": "ID del ítem (ej. TICKET-101) o URL completa del recurso.",
                },
                "provider_name": {
                    "type": "string",
                    "description": "Nombre del proveedor configurado (ej. 'youtrack').",
                },
            },
            "required": ["resource", "provider_name"],
        },
    },
    {
        "name": "read_summarize",
        "description": "Genera una versión condensada (resumen) de un ítem utilizando un LLM. "
        "Ideal para ahorrar tokens cuando solo se necesitan los puntos clave y el contexto.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource": {
                    "type": "string",
                    "description": "ID del ítem (ej. TICKET-101) o URL completa del recurso.",
                },
                "provider_name": {
                    "type": "string",
                    "description": "Nombre del proveedor (ej. 'youtrack').",
                },
                "max_tokens": {
                    "type": "integer",
                    "description": "Límite aproximado de tokens para el resumen "
                    "(min: 1, max: 10000).",
                    "default": 500,
                },
            },
            "required": ["resource", "provider_name"],
        },
    },
    {
        "name": "read_chunks",
        "description": "Divide un ítem extenso en fragmentos (chunks) manejables de máximo "
        "500 tokens cada uno. Úsalo para procesar o navegar por partes específicas de un "
        "ticket muy largo.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource": {
                    "type": "string",
                    "description": "ID del ítem (ej. TICKET-101) o URL completa del recurso.",
                },
                "provider_name": {
                    "type": "string",
                    "description": "Nombre del proveedor (ej. 'youtrack').",
                },
                "chunk_indices": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Opcional: Lista de índices de fragmentos a recuperar "
                    "(ej. [1, 3]). Si se omite, devuelve todos los fragmentos disponibles.",
                },
            },
            "required": ["resource", "provider_name"],
        },
    },
]
