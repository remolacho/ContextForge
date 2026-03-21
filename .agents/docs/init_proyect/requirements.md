# Documento de Requisitos

## Introducción

Este documento describe los requisitos para **ContextForge**, un servidor MCP (Model Context Protocol) dockerizado en Python cuyo propósito principal es **optimizar el consumo de tokens** al proporcionar contexto preciso a agentes de AI. El servidor está diseñado para ser usado por desarrolladores que integran agentes de AI (como Cursor) en su flujo de trabajo: el desarrollador configura el MCP en su agente y ContextForge recibe esa configuración automáticamente al iniciar la sesión.

ContextForge adopta una arquitectura **multi-proveedor**: permite configurar múltiples fuentes de contexto simultáneamente y está preparado para soportar en el futuro proveedores de repositorios (GitHub, GitLab) y archivos (PDF, Markdown). Para el **MVP**, el alcance funcional se limita a la lectura de tareas desde proveedores de tipo Task (YouTrack como implementación inicial).

El servidor expone tres herramientas **genéricas e independientes del proveedor**: `read_full`, `read_chunks` y `read_summarize`, con caché persistente en ChromaDB. Los proveedores se configuran **desde el cliente implementador** (ej. Cursor) al registrar el MCP, y ContextForge los recibe en el mensaje de inicialización MCP via HTTP, siguiendo el estándar **Streamable HTTP** (spec 2025-03-26). El motor LLM se configura en el servidor mediante variables de entorno (`LLM_ENGINE`, `LLM_API_KEY`), manteniendo un `LLMFactory` que permite cambiar de motor sin modificar la lógica de negocio.

Ejemplo de configuración que el cliente envía al servidor:

```json
{
  "providers": {
    "youtrack": { "base_url": "https://company.youtrack.cloud", "token": "perm_xxx" },
    "github":   { "token": "ghp_xxx" },
    "gitlab":   { "base_url": "https://gitlab.com", "token": "glpat_xxx" }
  }
}
```

## Glosario

- **ContextForge**: El servidor MCP principal que implementa el protocolo MCP y expone las herramientas a los clientes.
- **Tool**: Función genérica expuesta por ContextForge que puede ser invocada por un agente de AI, independiente del proveedor de origen.
- **AI_Agent**: Cliente de ContextForge, como Cursor u otro agente de AI, que invoca las herramientas para obtener contexto preciso minimizando el consumo de tokens.
- **Provider**: Abstracción genérica sobre una fuente de contexto. En el MVP, los proveedores son de tipo Task (ej. YouTrack).
- **TaskProvider**: Proveedor especializado en sistemas de gestión de tareas (YouTrack, Jira, etc.).
- **ProviderFactory**: Componente que recibe el tipo de proveedor y sus credenciales, e instancia la clase concreta correspondiente.
- **LLMFactory**: Componente que recibe el tipo de motor LLM (ej. "gemini", "openai") y su API key, e instancia la clase concreta correspondiente.
- **LLMEngine**: Abstracción genérica sobre un motor de lenguaje natural. Implementaciones: Gemini, OpenAI, etc.
- **SessionConfig**: Objeto que contiene la configuración de proveedores enviada por el cliente al iniciar la sesión MCP. Se recibe en el mensaje `initialize` del protocolo MCP via HTTP y se almacena en memoria por sesión.
- **LLMConfig**: Configuración del motor LLM leída desde variables de entorno del servidor: tipo de motor (`LLM_ENGINE`) y API key (`LLM_API_KEY`).
- **ProviderConfig**: Configuración de un proveedor específico dentro de `SessionConfig`: `base_url` (opcional según proveedor) y `token` de autenticación. El nombre del proveedor es la clave del mapa `providers`.
- **ChromaDB_Repository**: Componente responsable de interactuar con la base de datos vectorial ChromaDB.
- **CacheManager**: Componente responsable de verificar y gestionar la caché en ChromaDB.
- **ContextItem**: Objeto genérico que representa un ítem de contexto recuperado de cualquier proveedor, con ID, contenido y metadatos.
- **Chunk**: Fragmento de texto de un ContextItem con un máximo de 500 tokens, identificado por su índice dentro del conjunto total.
- **content_hash**: Hash SHA-256 del contenido completo del ContextItem tal como es retornado por el proveedor. Se usa junto con el `item_id` y `provider_name` como clave de caché compuesta.
- **Chunk_Index**: Número entero que identifica la posición de un Chunk dentro del conjunto total, comenzando en 1.
- **Token**: Unidad mínima de procesamiento de texto según el tokenizador del motor LLM activo.

---

## Requisitos

### Requisito 1: Inicialización de sesión y configuración multi-proveedor via MCP HTTP

**User Story:** Como desarrollador que configura ContextForge en mi agente de AI (ej. Cursor), quiero definir los proveedores y el motor LLM en el archivo de configuración MCP de mi cliente, para que el servidor los reciba automáticamente al iniciar la sesión sin necesidad de variables de entorno adicionales.

#### Criterios de Aceptación

1. THE ContextForge SHALL implementar el transporte **Streamable HTTP** (spec MCP 2025-03-26), exponiendo un único endpoint HTTP que soporte métodos POST y GET.
2. WHEN el AI_Agent envía el mensaje de inicialización MCP (`initialize`), THE ContextForge SHALL leer la `SessionConfig` del campo `params.clientInfo.config` del body JSON-RPC, con la siguiente estructura:
   ```json
   {
     "providers": {
       "<provider_name>": { "base_url": "<url>", "token": "<token>" }
     }
   }
   ```
3. WHEN la `SessionConfig` es recibida y validada, THE ContextForge SHALL almacenarla en memoria asociada a la sesión activa y reutilizarla para todas las invocaciones de herramientas de esa sesión.
4. IF el campo `providers` está ausente o vacío en la `SessionConfig`, THEN THE ContextForge SHALL retornar un error de inicialización MCP indicando que se requiere al menos un proveedor configurado.
4. IF un proveedor en `providers` tiene `token` vacío o ausente, THEN THE ContextForge SHALL retornar un error indicando qué proveedor tiene la configuración incompleta.
5. IF la `base_url` de un proveedor que la requiere tiene un formato inválido (no HTTP/HTTPS), THEN THE ContextForge SHALL retornar un error descriptivo indicando el proveedor afectado.
6. THE ContextForge SHALL validar el header `Origin` en todas las conexiones entrantes para prevenir ataques de DNS rebinding, conforme al estándar MCP Streamable HTTP.

---

### Requisito 2: Configuración del motor LLM via variables de entorno

**User Story:** Como operador del sistema, quiero configurar el motor LLM (ej. "gemini", "openai") y su API key mediante variables de entorno del servidor, para que ContextForge use ese motor en todas las sesiones sin que los clientes necesiten proveerlo.

#### Criterios de Aceptación

1. THE ContextForge SHALL leer el tipo de motor LLM desde la variable de entorno `LLM_ENGINE` (ej. "gemini", "openai") y la API key desde `LLM_API_KEY` al iniciar el servidor.
2. WHEN ContextForge inicia, THE LLMFactory SHALL instanciar el motor LLM correspondiente al valor de `LLM_ENGINE` usando `LLM_API_KEY` como credencial.
3. IF `LLM_ENGINE` no está definida, THE ContextForge SHALL usar "gemini" como valor por defecto y registrar un aviso en los logs.
4. IF `LLM_API_KEY` no está definida al iniciar, THEN THE ContextForge SHALL registrar un error en los logs y detener el proceso con código de salida distinto de cero.
5. IF el valor de `LLM_ENGINE` no tiene una implementación registrada en el `LLMFactory`, THEN THE ContextForge SHALL registrar un error en los logs y detener el proceso con código de salida distinto de cero, listando los motores disponibles.
6. WHEN se agrega un nuevo motor LLM, THE LLMFactory SHALL ser capaz de instanciarlo sin modificar la lógica de los casos de uso ni de las herramientas.
7. THE LLMFactory SHALL usar un registro dinámico que permita registrar nuevos motores sin modificar el factory (Open/Closed Principle).

---

### Requisito 3: Herramienta de lectura completa (`read_full`)

**User Story:** Como AI_Agent, quiero leer el contenido completo de un ítem de contexto por su ID y proveedor, para obtener toda la información disponible cuando necesito el contexto íntegro.

#### Criterios de Aceptación

1. WHEN el AI_Agent invoca `read_full` con un `item_id` y `provider_name` válidos, THE ContextForge SHALL resolver el proveedor desde la `SessionConfig` usando `provider_name` como clave, instanciarlo via `ProviderFactory` y recuperar el contenido completo del ítem.
2. WHEN el ítem es recuperado exitosamente, THE ContextForge SHALL retornar el texto completo del ítem al AI_Agent.
3. WHEN el ítem es recuperado exitosamente, THE ChromaDB_Repository SHALL almacenar el contenido completo junto con los metadatos `{item_id, provider_name, content_hash, tool: "read_full", timestamp}`.
4. WHEN el CacheManager detecta que existe en ChromaDB una entrada con el mismo `item_id`, `provider_name`, `content_hash` y `tool: "read_full"`, THE ContextForge SHALL retornar el contenido almacenado en caché sin consultar al proveedor.
5. IF el `provider_name` no está en la `SessionConfig`, THEN THE ContextForge SHALL retornar un error indicando los proveedores disponibles en la sesión actual.
6. IF el `item_id` no existe en el proveedor, THEN THE ContextForge SHALL retornar un error descriptivo indicando que el ítem no fue encontrado.
7. IF el proveedor retorna un error de autenticación, THEN THE ContextForge SHALL retornar un error indicando que el token de autenticación es inválido o ha expirado.

---

### Requisito 4: Herramienta de resumen (`read_summarize`)

**User Story:** Como AI_Agent, quiero obtener un resumen de los puntos más importantes de un ítem de contexto con un límite de tokens configurable, para obtener contexto conciso consumiendo la menor cantidad de tokens posible.

#### Criterios de Aceptación

1. WHEN el AI_Agent invoca `read_summarize` con un `item_id` y `provider_name` válidos, THE ContextForge SHALL resolver el proveedor desde la `SessionConfig`, instanciarlo via `ProviderFactory` y recuperar el contenido completo del ítem.
2. WHEN el AI_Agent invoca `read_summarize` sin especificar `max_tokens`, THE ContextForge SHALL usar 500 como valor por defecto.
3. WHEN el AI_Agent invoca `read_summarize` con un `max_tokens` explícito, THE LLMEngine SHALL generar un resumen del contenido respetando el límite de tokens indicado.
4. WHEN el resumen es generado exitosamente, THE ContextForge SHALL retornar el resumen al AI_Agent.
5. WHEN el resumen es generado exitosamente, THE ChromaDB_Repository SHALL almacenar el resumen junto con los metadatos `{item_id, provider_name, content_hash, tool: "read_summarize", max_tokens, timestamp}`.
6. WHEN el CacheManager detecta que existe en ChromaDB una entrada con el mismo `item_id`, `provider_name`, `content_hash`, `tool: "read_summarize"` y el mismo `max_tokens`, THE ContextForge SHALL retornar el resumen almacenado en caché sin consultar al proveedor ni al LLMEngine.
7. IF el `max_tokens` proporcionado es menor a 1 o mayor a 10000, THEN THE ContextForge SHALL retornar un error indicando que el valor debe estar entre 1 y 10000.
8. IF el `item_id` no existe en el proveedor, THEN THE ContextForge SHALL retornar un error descriptivo indicando que el ítem no fue encontrado.

---

### Requisito 5: Herramienta de fragmentación (`read_chunks`)

**User Story:** Como AI_Agent, quiero dividir el contenido de un ítem en fragmentos de máximo 500 tokens y poder solicitar únicamente los fragmentos específicos que necesito, para consumir solo el contexto relevante y minimizar el uso de tokens.

#### Criterios de Aceptación

1. WHEN el AI_Agent invoca `read_chunks` con un `item_id` y `provider_name` válidos, THE ContextForge SHALL resolver el proveedor desde la `SessionConfig`, instanciarlo via `ProviderFactory` y recuperar el contenido completo del ítem.
2. WHEN el contenido del ítem es recuperado, THE ContextForge SHALL dividir el contenido en Chunks de máximo 500 tokens cada uno, asignando un Chunk_Index secuencial comenzando en 1.
3. WHEN el AI_Agent invoca `read_chunks` sin especificar índices, THE ContextForge SHALL retornar todos los Chunks disponibles, incluyendo el Chunk_Index de cada Chunk y el total de Chunks generados.
4. WHEN el AI_Agent invoca `read_chunks` especificando una lista de Chunk_Index (por ejemplo, [1, 2] o [3, 5]), THE ContextForge SHALL retornar únicamente los Chunks correspondientes a los índices solicitados, junto con el total de Chunks del ítem.
5. WHEN los Chunks son generados, THE ChromaDB_Repository SHALL almacenar cada Chunk individualmente con los metadatos `{item_id, provider_name, content_hash, tool: "read_chunks", chunk_index, total_chunks, timestamp}`.
6. WHEN el CacheManager detecta que existe en ChromaDB una entrada con el mismo `item_id`, `provider_name`, `content_hash` y `tool: "read_chunks"`, THE ContextForge SHALL recuperar los Chunks desde caché sin consultar al proveedor y retornar únicamente los índices solicitados.
7. IF el AI_Agent solicita un Chunk_Index que no existe para el ítem, THEN THE ContextForge SHALL retornar un error descriptivo indicando los índices válidos disponibles (de 1 a total_chunks).
8. IF el `item_id` no existe en el proveedor, THEN THE ContextForge SHALL retornar un error descriptivo indicando que el ítem no fue encontrado.
9. THE ContextForge SHALL preservar la coherencia semántica al dividir el contenido, evitando cortar oraciones a la mitad cuando sea posible.

---

### Requisito 6: Gestión de caché y deduplicación

**User Story:** Como AI_Agent, quiero que el servidor evite consultas redundantes al proveedor y al LLM cuando ya existe una respuesta válida en caché, para reducir la latencia y minimizar el consumo de tokens en cada invocación.

#### Criterios de Aceptación

1. WHEN el CacheManager recibe una solicitud, THE CacheManager SHALL consultar ChromaDB verificando si existe una entrada con los mismos `item_id`, `provider_name`, `content_hash` y `tool` en los metadatos.
2. WHEN el CacheManager verifica una solicitud de `read_summarize`, THE CacheManager SHALL comparar también el valor de `max_tokens` además de los campos anteriores.
3. WHEN el CacheManager encuentra una entrada válida en caché, THE ContextForge SHALL retornar el contenido cacheado con un indicador `from_cache: true`.
4. WHEN el CacheManager no encuentra una entrada válida en caché, THE ContextForge SHALL ejecutar el flujo completo de la herramienta solicitada.
5. WHEN el `content_hash` del ítem recuperado del proveedor difiere del `content_hash` almacenado en caché para el mismo `item_id`, `provider_name` y `tool`, THE CacheManager SHALL invalidar la entrada existente y ejecutar el flujo completo.
6. THE CacheManager SHALL operar de forma transparente sin requerir configuración adicional por parte del AI_Agent.

---

### Requisito 7: ProviderFactory y extensibilidad de proveedores

**User Story:** Como desarrollador, quiero que la arquitectura soporte la adición de nuevos proveedores de contexto sin modificar la lógica existente, para poder integrar YouTrack, Jira, GitHub u otras fuentes en el futuro.

#### Criterios de Aceptación

1. THE ProviderFactory SHALL definir un registro dinámico que mapee tipos de proveedor (strings) a clases concretas que implementen la interfaz `ProviderInterface`.
2. THE ProviderFactory SHALL exponer un método `create(provider_type: str, config: ProviderConfig) -> ProviderInterface` que instancie el proveedor correcto.
3. IF el `provider_type` no está registrado, THEN THE ProviderFactory SHALL lanzar `ProviderNotRegisteredError` con un mensaje que lista los tipos disponibles.
4. WHEN se agrega un nuevo proveedor, THE sistema SHALL ser capaz de usarlo registrándolo en el factory sin modificar la lógica de las herramientas ni del CacheManager.
5. THE `ProviderInterface` SHALL definir los métodos abstractos `get_item(item_id: str, config: ProviderConfig) -> ContextItem` y `validate_config(config: ProviderConfig) -> bool` como contrato obligatorio para todas las implementaciones.
6. THE YouTrackProvider SHALL implementar `ProviderInterface` como la implementación funcional del MVP.
7. WHEN se agrega un proveedor de tipo repositorio o archivo en el futuro, THE herramientas `read_full`, `read_chunks` y `summarize` SHALL funcionar sin modificaciones.

---

### Requisito 8: LLMFactory y extensibilidad de motores LLM

**User Story:** Como desarrollador, quiero que el motor LLM sea intercambiable mediante configuración, para poder usar Gemini, OpenAI u otros motores sin modificar la lógica de negocio.

#### Criterios de Aceptación

1. THE LLMFactory SHALL definir un registro dinámico que mapee tipos de motor (strings como "gemini", "openai") a clases concretas que implementen `LLMEngineInterface`.
2. THE LLMFactory SHALL exponer un método `create(engine_type: str, config: LLMConfig) -> LLMEngineInterface` que instancie el motor correcto.
3. IF el `engine_type` no está registrado, THEN THE LLMFactory SHALL lanzar `LLMEngineNotRegisteredError` con un mensaje que lista los motores disponibles.
4. THE `LLMEngineInterface` SHALL definir los métodos abstractos `summarize(content: str, max_tokens: int) -> str` y `count_tokens(text: str) -> int` como contrato obligatorio.
5. THE GeminiLLMEngine SHALL implementar `LLMEngineInterface` como la implementación funcional del MVP, usando LangChain como framework de orquestación.
6. WHEN el LLMEngine genera un resumen, THE LLMEngine SHALL usar un prompt estructurado que indique el límite de tokens y solicite los puntos más importantes del ítem.
7. IF el LLMEngine recibe un error de cuota o límite de la API, THEN THE LLMEngine SHALL lanzar `LLMError` con un mensaje descriptivo indicando que se superó el límite de la API.

---

### Requisito 9: Integración con YouTrack (MVP)

**User Story:** Como usuario de ContextForge, quiero que el servidor se conecte a la API de YouTrack usando el token y la URL configurados, para recuperar el contenido completo de las tareas.

#### Criterios de Aceptación

1. WHEN el YouTrackProvider recibe un `item_id`, THE YouTrackProvider SHALL realizar una solicitud HTTP GET a la API REST de YouTrack usando la `ProviderConfig` correspondiente.
2. THE YouTrackProvider SHALL incluir el token de autenticación en el encabezado `Authorization: Bearer {token}` de cada solicitud.
3. WHEN YouTrack retorna una respuesta exitosa, THE YouTrackProvider SHALL extraer el título, descripción, comentarios y campos personalizados de la tarea y retornarlos como un objeto `ContextItem`.
4. IF YouTrack retorna un código de estado HTTP 401 o 403, THEN THE YouTrackProvider SHALL lanzar `AuthenticationError` con un mensaje descriptivo.
5. IF YouTrack retorna un código de estado HTTP 404, THEN THE YouTrackProvider SHALL lanzar `ItemNotFoundError` con el `item_id` en el mensaje.
6. IF YouTrack retorna un código de estado HTTP 5xx, THEN THE YouTrackProvider SHALL lanzar `ProviderServerError` con el código de estado en el mensaje.

---

### Requisito 10: Integración con ChromaDB

**User Story:** Como operador del sistema, quiero que los datos procesados se persistan en ChromaDB dockerizada con un volumen local, para que la caché sobreviva reinicios del contenedor.

#### Criterios de Aceptación

1. THE ChromaDB_Repository SHALL conectarse a una instancia de ChromaDB accesible mediante host y puerto configurables por variable de entorno.
2. THE ChromaDB_Repository SHALL usar una colección única `contextforge_cache` con filtrado por metadatos.
3. WHEN ChromaDB no está disponible al iniciar ContextForge, THE ContextForge SHALL registrar un error en los logs y detener el proceso con código de salida distinto de cero.
4. THE ChromaDB_Repository SHALL almacenar embeddings generados por el LLMEngine activo junto con el contenido textual y los metadatos de cada entrada.
5. WHERE el volumen Docker está configurado, THE ChromaDB_Repository SHALL persistir todos los datos en el directorio montado para sobrevivir reinicios del contenedor.

---

### Requisito 11: Infraestructura Docker

**User Story:** Como operador del sistema, quiero que tanto ContextForge como ChromaDB estén dockerizados con un volumen de persistencia, para facilitar el despliegue y garantizar la durabilidad de los datos.

#### Criterios de Aceptación

1. THE ContextForge SHALL estar empaquetado en una imagen Docker basada en Python 3.11 con todas las dependencias instaladas.
2. THE ContextForge SHALL leer únicamente la configuración de ChromaDB (`CHROMA_HOST`, `CHROMA_PORT`) y el puerto del servidor (`MCP_PORT`) desde variables de entorno. La configuración de proveedores y motor LLM se recibe por sesión MCP, no por variables de entorno.
3. WHERE Docker Compose está disponible, THE ContextForge SHALL definir un `docker-compose.yml` que incluya el servicio `contextforge` y el servicio `chromadb` en la misma red `contextforge-net`.
4. WHERE Docker Compose está disponible, THE ContextForge SHALL definir un volumen Docker nombrado `chroma-data` para persistir los datos de ChromaDB.
5. THE ContextForge SHALL incluir un entorno virtual Python (`.venv`) para el desarrollo local fuera de Docker.
6. IF una variable de entorno requerida del servidor (`CHROMA_HOST`, `CHROMA_PORT`) no está definida al iniciar el contenedor, THE ContextForge SHALL usar los valores por defecto (`chromadb` y `8000` respectivamente) y registrar un aviso en los logs.

---

### Requisito 12: Integración con agentes de AI (Cursor y otros)

**User Story:** Como desarrollador, quiero agregar ContextForge a mi agente de AI (como Cursor) configurando proveedores y motor LLM en el archivo MCP de mi cliente, para que el agente pueda solicitar contexto preciso consumiendo solo los tokens necesarios.

#### Criterios de Aceptación

1. THE ContextForge SHALL exponer sus herramientas siguiendo el protocolo MCP estándar con transporte Streamable HTTP, de forma que cualquier AI_Agent compatible pueda descubrirlas e invocarlas.
2. THE ContextForge SHALL ser configurable desde el cliente mediante un JSON estándar enviado en el mensaje `initialize`, con la siguiente estructura de ejemplo:
   ```json
   {
     "mcpServers": {
       "ContextForge": {
         "url": "http://localhost:3000/mcp",
         "config": {
           "providers": {
             "youtrack": { "base_url": "https://company.youtrack.cloud", "token": "perm_xxx" },
             "github":   { "token": "ghp_xxx" },
             "gitlab":   { "base_url": "https://gitlab.com", "token": "glpat_xxx" }
           }
         }
       }
     }
   }
   ```
3. WHEN un AI_Agent invoca una herramienta, THE ContextForge SHALL retornar únicamente el contexto solicitado, sin incluir información adicional no requerida, para minimizar el consumo de tokens.
4. THE ContextForge SHALL incluir en la descripción de cada herramienta información suficiente para que el AI_Agent pueda decidir qué herramienta usar según la cantidad de contexto que necesita (completo con `read_full`, resumido con `read_summarize`, o fragmentado con `read_chunks`).
5. WHEN el AI_Agent invoca `read_chunks` con índices específicos, THE ContextForge SHALL retornar solo esos fragmentos, permitiendo al AI_Agent obtener contexto incremental.
