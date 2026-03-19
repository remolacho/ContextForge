# Plan de Implementación: ContextForge

> **Nota:** Consultar el Issue #2 que contiene la documentación de Design y Requirements antes de crear las tareas de implementación.

## Visión General

Implementación incremental de ContextForge siguiendo Clean Architecture: primero el dominio, luego infraestructura, después la capa de aplicación y finalmente la interfaz HTTP/MCP. Cada tarea construye sobre la anterior y termina con la integración completa.

> **Para dev junior:** Lee el `design.md` antes de empezar. Cada tarea indica el archivo a crear, qué debe contener y por qué existe. Las tareas marcadas con `*` son opcionales (property tests) pero muy recomendadas.

## Tareas

- [ ] 1. Configurar estructura del proyecto y dependencias
  > Prepara el esqueleto del proyecto: archivos de configuración, dependencias Python, Docker y todos los directorios vacíos. Sin esto, nada más puede ejecutarse. Es la base sobre la que se construye todo.
  - Crear `pyproject.toml` con dependencias: `fastapi`, `uvicorn`, `pydantic-settings`, `chromadb`, `langchain`, `langchain-google-genai`, `langchain-core`, `requests`, `hypothesis`, `pytest`, `pytest-asyncio`
  - Crear `requirements.txt` generado desde `pyproject.toml` (ejecutar `pip-compile` o exportar manualmente)
  - Crear `.env.example` documentando todas las variables: `LLM_ENGINE`, `LLM_API_KEY`, `CHROMA_HOST`, `CHROMA_PORT`, `MCP_PORT`, `LOG_LEVEL`
  - Crear `Dockerfile` basado en `python:3.11-slim` con `PYTHONPATH=/app` para que los imports funcionen desde la raíz
  - Crear `docker-compose.yml` con dos servicios: `contextforge` (puerto 8999) y `chromadb` (puerto 9000→8000), conectados en red `contextforge-net`, con volumen `chroma-data` para persistencia
  - Crear todos los directorios y archivos `__init__.py` vacíos según la estructura del `design.md` (sin `__init__.py` Python no reconoce los módulos)
  - _Ver `requirements.md`: Req. 11 — Infraestructura Docker (criterios 1-5)_

- [ ] 2. Implementar Domain Layer
  > El dominio es el núcleo del sistema: define qué datos existen, qué contratos deben cumplir los componentes y qué errores pueden ocurrir. No depende de ninguna librería externa. Si el dominio está bien definido, el resto del código es predecible.

  - [ ] 2.1 Crear entidades de dominio
    > Las entidades son los objetos de datos que viajan por todo el sistema. Usar `@dataclass` de Python para definirlas de forma limpia sin boilerplate.
    - Implementar `src/domain/entities.py` con las siguientes dataclasses:
      - `ProviderConfig`: guarda `code` ("youtrack", "jira"), `token` y `base_url` opcional de un proveedor
      - `SessionConfig`: contiene un dict `providers` donde la clave es el nombre del proveedor y el valor es su `ProviderConfig`
      - `LLMConfig`: guarda `engine_type` (ej. "gemini") y `api_key` para el motor LLM
      - `ContextItem`: representa un ítem recuperado del proveedor con `item_id`, `title`, `description`, `comments`, `custom_fields`, `raw_content` (texto concatenado) y `content_hash` (SHA-256)
      - `Chunk`: representa un fragmento de texto con `chunk_index` (empieza en 1), `total_chunks`, `content` y `token_count`
      - `CacheEntry`: representa una entrada en caché con `item_id`, `provider_name`, `content_hash`, `tool`, `content`, `metadata` y `from_cache: bool`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§2), Req. 3 — read_full (§1), Req. 4 — read_summarize (§1), Req. 5 — read_chunks (§2)_

  - [ ] 2.2 Crear interfaces (ports) de dominio
    > Las interfaces definen los contratos que deben cumplir las implementaciones concretas. Permiten que los casos de uso no dependan de ChromaDB, YouTrack o Gemini directamente, sino de abstracciones. Esto facilita testear con mocks y cambiar implementaciones sin tocar la lógica de negocio.
    - Implementar `src/domain/interfaces.py` con tres ABCs (clases abstractas):
      - `ProviderInterface`: contrato para proveedores de datos. Métodos: `get_item(item_id, config) → ContextItem` y `validate_config(config) → bool`
      - `CacheRepositoryInterface`: contrato para el repositorio de caché. Métodos: `lookup(item_id, provider_name, content_hash, tool, **kwargs) → CacheEntry | None`, `store(entry)` e `invalidate(item_id, provider_name, tool)`
      - `LLMEngineInterface`: contrato para el motor LLM. Métodos: `summarize(content, max_tokens) → str`, `count_tokens(text) → int` y `get_embeddings(text) → list[float]`
    - _Ver `requirements.md`: Req. 7 — ProviderFactory (§5), Req. 8 — LLMFactory (§4)_

  - [ ] 2.3 Crear jerarquía de excepciones de dominio
    > Tener excepciones propias del dominio permite que los exception handlers de FastAPI capturen errores específicos y devuelvan el código HTTP correcto. Sin esto, todos los errores serían genéricos 500.
    - Implementar `src/domain/exceptions.py` con toda la jerarquía bajo `ContextForgeError` (clase base):
      - `ConfigurationError`: error de configuración general
      - `SessionConfigError`: sesión MCP inválida o no encontrada → HTTP 400
      - `AuthenticationError`: token inválido o expirado → HTTP 401
      - `ItemNotFoundError`: ítem no existe en el proveedor → HTTP 404
      - `ProviderServerError`: el proveedor respondió con 5xx
      - `CacheError`: error al leer/escribir en ChromaDB
      - `LLMError`: error al llamar al motor LLM
      - `ValidationError`: parámetro inválido (ej. `max_tokens` fuera de rango) → HTTP 422
      - `ProviderNotRegisteredError`: se pidió un proveedor que no está registrado en el factory → HTTP 422
      - `LLMEngineNotRegisteredError`: se pidió un motor LLM que no está registrado
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§4), Req. 3 — read_full (§5,6,7), Req. 4 — read_summarize (§7), Req. 5 — read_chunks (§7), Req. 7 — ProviderFactory (§3), Req. 8 — LLMFactory (§3)_


- [ ] 3. Configurar linting y Makefile
  > Configurar herramientas de calidad de código desde el inicio evita acumular deuda técnica. Un `Makefile` centraliza los comandos más usados para que cualquier dev pueda correr linting, tests o levantar el proyecto con un solo comando sin tener que recordar flags.
  - Agregar dependencias de desarrollo en `pyproject.toml`: `ruff` (linter + formatter rápido), `mypy` (type checking)
  - Crear `ruff.toml` o sección `[tool.ruff]` en `pyproject.toml` con configuración básica:
    - `line-length = 100`
    - `select = ["E", "F", "I"]` (errores, pyflakes, imports)
    - `exclude = [".venv", "__pycache__"]`
  - Crear `Makefile` en la raíz con los siguientes targets:
    - `make lint` → ejecuta `ruff check .` (muestra todos los problemas encontrados, no modifica nada)
    - `make fix` → ejecuta `ruff check --fix .` (corrige automáticamente lo que puede: imports sin usar, comillas, espacios, etc. Lo que no puede corregir solo lo reporta para revisión manual)
    - `make lint-file FILE=ruta/archivo.py` → ejecuta `ruff check $(FILE)` (lint sobre un archivo o directorio específico, útil para revisar solo lo que estás tocando)
    - `make format` → ejecuta `ruff format .` (formatea el estilo del código: indentación, saltos de línea, etc.)
    - `make typecheck` → ejecuta `mypy src/ app/` (verifica tipos estáticos, estos errores siempre son manuales ya que mypy no autocorrige)
    - `make test` → ejecuta `pytest tests/ -v`
    - `make check` → ejecuta `lint` + `typecheck` + `test` en secuencia (útil antes de hacer commit)
    - `make up` → ejecuta `docker-compose up --build`
    - `make down` → ejecuta `docker-compose down`

- [ ] 4. Implementar Infrastructure Layer: Builders
  > Los builders construyen objetos complejos paso a paso usando una API fluida (encadenamiento de métodos). Evitan constructores con muchos parámetros y centralizan la lógica de construcción (ej. calcular el hash SHA-256 siempre en el mismo lugar).

  - [ ] 4.1 Implementar `ContextItemBuilder`
    > Este builder debe ser **genérico y agnóstico al proveedor**. Cada proveedor es responsable de transformar su respuesta JSON específica a campos genéricos antes de pasarlos al builder. Esto cumple con el principio Open/Closed: agregar un nuevo proveedor (Jira, GitHub, etc.) no requiere modificar el builder.
    - Crear `src/infrastructure/builders/context_item.py` con métodos fluidos:
      - `set_item_id(item_id)`: guarda el ID del ítem
      - `set_provider_name(name)`: guarda el nombre del proveedor
      - `set_title(title)`: guarda el título
      - `set_description(description)`: guarda la descripción
      - `set_comments(comments: list[str])`: guarda la lista de comentarios
      - `set_custom_fields(custom_fields: dict)`: guarda campos personalizados
      - `build()`: concatena título + descripción + comentarios en `raw_content`, calcula `content_hash` como SHA-256 de `raw_content` y retorna el `ContextItem`
    - **NO** debe tener métodos como `from_youtrack_response()` - eso violaría el principio Open/Closed
    - _Ver `requirements.md`: Req. 9 — Integración YouTrack (§3), Req. 6 — Caché (§1)_

  - [ ] 4.2 Escribir property test para ContextItemBuilder
    > Verifica que el hash SHA-256 siempre es el mismo para el mismo contenido (determinismo) y diferente para contenido diferente.
    - Archivo: `tests/property/test_properties_providers.py`
    - **Propiedad 20:** Para cualquier combinación de título, descripción y comentarios, `build()` siempre produce el mismo `content_hash` (SHA-256 determinista). Si cambia cualquier campo, el hash cambia.
    - Usar `@given(st.text(), st.text(), st.lists(st.text()))` de hypothesis con `@settings(max_examples=100)`
    - Comentario en el test: `# Feature: contextforge, Propiedad 20: ContextItemBuilder produce content_hash SHA-256 consistente`
    - _Valida: Requisito 6.1_

  - [ ] 4.3 Implementar `CacheEntryBuilder`
    > Construye una `CacheEntry` completa con todos sus metadatos de forma legible. Evita crear el objeto con un constructor de 7 parámetros.
    - Crear `src/infrastructure/builders/cache_entry.py` con métodos fluidos:
      - `for_item(item: ContextItem)`: copia `item_id`, `provider_name` y `content_hash` del ítem
      - `with_tool(tool: str)`: establece la herramienta (`"read_full"`, `"read_summarize"`, `"read_chunks"`)
      - `with_content(content: str)`: establece el contenido a cachear
      - `with_metadata(**kwargs)`: agrega metadatos adicionales (ej. `timestamp`, `max_tokens`)
      - `build()`: retorna el `CacheEntry` con `from_cache=False`
    - _Ver `requirements.md`: Req. 3 — read_full (§3), Req. 4 — read_summarize (§5), Req. 5 — read_chunks (§5)_

- [ ] 5. Implementar Infrastructure Layer: Factories
  > Los factories crean instancias de proveedores y motores LLM basándose en el código/tipo recibido en la configuración. Es un enfoque simple: `ProviderFactory` usa `config.code` para saber qué clase instanciar, `LLMFactory` usa `config.engine_type`.

  - [ ] 5.1 Implementar `ProviderFactory`
    > Factory simple que instancia el proveedor según `config.code`. No requiere registro previo; cada proveedor se agrega directamente en el código.
    - Crear `src/infrastructure/providers/factory.py`:
      - Clase `ProviderFactory` con constructor que recibe `config: ProviderConfig`
      - Método `create()` que usa `if/elif` basado en `config.code`:
        - `code == "youtrack"` → retorna `YouTrackProvider(self.config)`
        - Si no coincide → lanza `ProviderNotRegisteredError`
    - _Ver `requirements.md`: Req. 7 — ProviderFactory (§1,2,3,4)_

  - [ ]* 5.2 Escribir property test para ProviderFactory
    > Verifica que el factory instancia la clase correcta según `config.code`.
    - Archivo: `tests/property/test_properties_providers.py`
    - Test: `ProviderFactory(config).create()` retorna `YouTrackProvider` para `code="youtrack"`
    - Test: `ProviderFactory(config).create()` lanza `ProviderNotRegisteredError` para code desconocido
    - _Valida: Requisito 7.3_

  - [ ] 5.3 Implementar `LLMFactory`
    > Factory simple que instancia el motor según `config.engine_type`. No requiere registro previo.
    - Crear `src/infrastructure/llm/factory.py`:
      - Clase `LLMFactory` con constructor que recibe `config: LLMConfig`
      - Método `create()` que usa `if/elif` basado en `config.engine_type`:
        - `engine_type == "gemini"` → retorna `GeminiLLMEngine(self.config)`
        - Si no coincide → lanza `LLMEngineNotRegisteredError`
    - _Ver `requirements.md`: Req. 8 — LLMFactory (§1,2,3,7)_

  - [ ]* 5.4 Escribir property test para LLMFactory
    > Verifica que el factory instancia la clase correcta según `config.engine_type`.
    - Archivo: `tests/property/test_properties_providers.py`
    - Test: `LLMFactory(config).create()` retorna `GeminiLLMEngine` para `engine_type="gemini"`
    - Test: `LLMFactory(config).create()` lanza `LLMEngineNotRegisteredError` para engine desconocido
    - _Valida: Requisito 8.3_


- [ ] 6. Implementar Infrastructure Layer: Proveedores
  > Los proveedores son los adaptadores que saben cómo hablar con sistemas externos (YouTrack, Jira, etc.). Implementan `ProviderInterface` para que el resto del sistema no sepa ni le importe con qué API externa se está comunicando.

  - [ ] 6.1 Implementar `YouTrackProvider`
    > El único proveedor funcional del MVP. Hace una llamada HTTP a la API de YouTrack, maneja los errores de autenticación y construye el `ContextItem` usando el builder. **El proveedor es responsable de transformar su respuesta JSON específica a campos genéricos** antes de pasarlos al builder.
    - Crear `src/infrastructure/providers/task/youtrack.py` implementando `ProviderInterface`:
      - Constructor recibe `config: ProviderConfig` y lo guarda en `self._config`
      - `get_item(item_id, config)`: hace GET a `{config.base_url}/api/issues/{item_id}?fields=id,idReadable,summary,description` con header `Authorization: Bearer {config.token}`
      - Mapeo de errores HTTP: 401/403 → lanzar `AuthenticationError`, 404 → `ItemNotFoundError`, 5xx → `ProviderServerError`
      - Usar `ContextItemBuilder` para construir el `ContextItem` transformando el JSON de YouTrack a campos genéricos:
        - `set_item_id(item_id)`
        - `set_provider_name("youtrack")`
        - `set_title(data.get("summary", ""))`
        - `set_description(data.get("description", ""))`
        - `set_comments([])` (comentarios vienen en endpoint separado)
        - `set_custom_fields({})` (custom fields no disponibles en este endpoint)
        - `build()` (calcula SHA-256 automáticamente de título + descripción)
      - `validate_config(config)`: retorna `True` si `token` no está vacío y `base_url` es una URL válida
    - _Ver `requirements.md`: Req. 9 — Integración YouTrack (§1,2,3,4,5,6)_

  - [ ]* 6.2 Escribir unit tests para YouTrackProvider
    > Verifica que `validate_config()` retorna valores correctos y que `get_item()` maneja errores HTTP correctamente.
    - Archivo: `tests/unit/test_youtrack_provider.py`
    - Tests para `validate_config()`:
      - URL válida + token no vacío → `True`
      - URL inválida → `False`
      - Token vacío → `False`
      - URL None → `False`
    - Tests para `get_item()` con mock de `requests.Response`:
      - Status 401/403 → `AuthenticationError`
      - Status 404 → `ItemNotFoundError`
      - Status 5xx → `ProviderServerError`
    - _Ver `requirements.md`: Req. 9 — Integración YouTrack (§2,3)_

  - [ ] 6.3 Crear stubs de proveedores futuros
    > Crear los archivos vacíos ahora establece la estructura para escalar. Un stub implementa la interfaz pero lanza `NotImplementedError`, dejando claro que aún no está implementado. **Cuando se implementen, deberán transformar su JSON específico a campos genéricos usando ContextItemBuilder** (igual que YouTrackProvider).
    - Crear `src/infrastructure/providers/git/github.py`: `GitHubProvider` stub que lanza `NotImplementedError`
    - Crear `src/infrastructure/providers/git/gitlab.py`: `GitLabProvider` stub que lanza `NotImplementedError`
    - Crear `src/infrastructure/providers/file/pdf.py`: `PDFProvider` stub que lanza `NotImplementedError`
    - Crear `src/infrastructure/providers/file/markdown.py`: `MarkdownProvider` stub que lanza `NotImplementedError`
    - **Nota:** Jira se agregará directamente en `ProviderFactory.create()` cuando se implemente
    - _Ver `requirements.md`: Req. 7 — ProviderFactory (§4,7)_

- [ ] 7. Implementar Infrastructure Layer: LLM
  > Integra LangChain con Gemini para generar resúmenes. Usa el patrón LCEL (LangChain Expression Language) que encadena prompt → modelo → parser de forma declarativa y legible.

  - [ ] 7.1 Implementar prompts LangChain
    > Centralizar el prompt en un archivo dedicado evita duplicación y facilita ajustarlo sin tocar la lógica del engine. Usar `ChatPromptTemplate.from_messages` con roles `system`/`human` es la práctica recomendada de LangChain.
    - Crear `src/infrastructure/llm/prompts.py`:
      - Importar `ChatPromptTemplate` de `langchain_core.prompts`
      - Definir `SUMMARIZE_PROMPT` con el prompt técnico para IA:
        ```
        System: Eres un asistente técnico especializado en resumir contenido.
        Reglas: máximo {max_tokens} tokens, información verificable, no inventar, priorizar problema/contexto/puntos clave
        Human: Contenido a resumir: {content}
        ```
    - _Ver `requirements.md`: Req. 8 — LLMFactory (§6)_

  - [ ] 7.2 Refactorizar `GeminiLLMEngine`
    > Implementación concreta del motor LLM usando Gemini. Expone `.llm` y `.embeddings` para que `Summarized` los use internamente.
    - Refactorizar `src/infrastructure/llm/gemini.py` implementando `LLMEngineInterface`:
      - Constructor recibe solo `config: LLMConfig`
      - Inicializa `ChatGoogleGenerativeAI` y `GoogleGenerativeAIEmbeddings`
      - `@property llm`: retorna `ChatGoogleGenerativeAI`
      - `@property embeddings`: retorna `GoogleGenerativeAIEmbeddings`
      - Modelo configurable via `config.model_version` (default: `gemini-2.5-flash-lite`)
    - _Ver `requirements.md`: Req. 8 — LLMFactory (§5,6,7)_

  - [ ] 7.3 Implementar `Summarized`
    > Implementa `SummarizeEngineInterface`. Recibe un `LLMEngineInterface` y el template de prompt, construye la chain LCEL internamente.
    - Crear `src/infrastructure/llm/summarized.py` implementando `SummarizeEngineInterface`:
      - Constructor recibe `engine_llm: LLMEngineInterface` y `prompt_template: ChatPromptTemplate`
      - Extrae `self._llm = engine_llm.llm` y `self._embeddings = engine_llm.embeddings`
      - Construye chain LCEL: `prompt_template | self._llm | StrOutputParser()`
      - `summarize(content, max_tokens)`: invoca la chain LCEL
      - `count_tokens(text)`: retorna `self._llm.get_num_tokens(text)`
      - `get_embeddings(text)`: retorna `self._embeddings.embed_query(text)`
    - Actualizar `src/infrastructure/llm/factory.py` para crear `Summarized(engine_llm, SUMMARIZE_PROMPT)` y retornarlo
    - _Ver `requirements.md`: Req. 8 — LLMFactory (§5,6,7)_


- [ ] 8. Implementar Infrastructure Layer: ChromaCacheRepository
  > Implementa el repositorio de caché usando ChromaDB. Cada entrada se identifica por la combinación `item_id + provider_name + content_hash + tool`. Si el contenido del ítem cambia (nuevo `content_hash`), la caché no hace match y se regenera.

  - [ ] 8.1 Implementar `ChromaCacheRepository`
    > ChromaDB es una base de datos vectorial. Aquí la usamos principalmente como almacén de documentos con filtros por metadatos, no tanto por similitud semántica.
    - Crear `src/infrastructure/cache/chroma.py` implementando `CacheRepositoryInterface`:
      - Constructor: conectar con `chromadb.HttpClient(host=host, port=port)` y obtener/crear colección `contextforge_cache` con `get_or_create_collection()`
      - `lookup(item_id, provider_name, content_hash, tool, **kwargs)`: consultar la colección filtrando por metadatos `{"item_id": ..., "provider_name": ..., "content_hash": ..., "tool": ...}` más `max_tokens` si está en `kwargs`. Si hay resultado, retornar `CacheEntry` con `from_cache=True`. Si no, retornar `None`.
      - `store(entry)`: llamar `upsert()` con el documento, metadatos y un ID único generado por `_build_doc_id(entry)`
      - `invalidate(item_id, provider_name, tool)`: eliminar todas las entradas que coincidan con esos tres campos usando `delete(where={...})`
      - Función auxiliar `_build_doc_id(entry)`: construir un ID único como `f"{entry.item_id}:{entry.provider_name}:{entry.tool}:{entry.content_hash}"` (agregar `max_tokens` si aplica)
    - _Ver `requirements.md`: Req. 10 — ChromaDB (§1,2,4), Req. 6 — Caché (§1,2)_

  - [ ]* 8.2 Escribir unit tests para ChromaCacheRepository
    > Tests unitarios con mock de ChromaDB para verificar que los métodos llaman a la API de ChromaDB con los parámetros correctos.
    - Archivo: `tests/unit/test_chroma_cache.py`
    - Test `lookup` con cache hit: mock retorna un documento → verificar que se retorna `CacheEntry` con `from_cache=True`
    - Test `lookup` con cache miss: mock retorna lista vacía → verificar que se retorna `None`
    - Test `store`: verificar que `upsert` es llamado con los metadatos correctos (todos los campos de la `CacheEntry`)
    - Test `invalidate`: verificar que `delete` es llamado con el filtro `{"item_id": ..., "provider_name": ..., "tool": ...}`
    - _Ver `requirements.md`: Req. 10 — ChromaDB (§2), Req. 6 — Caché (§1)_

  - [ ] 9. Implementar Application Layer: Casos de Uso
    > Los casos de uso son el corazón de la lógica de negocio. **IMPORTANTE:** El flujo debe ser: 1) verificar caché PRIMERO, 2) si hay hit retornar, 3) si hay miss ir al proveedor, 4) procesar (si aplica con LLM), 5) guardar en caché, 6) retornar. Esto evita consultas redundantes al proveedor y al LLM.

    - [ ] 9.1 Implementar `ReadFullUseCase`
      > Devuelve el texto completo del ítem. El flujo híbrido garantiza datos siempre actualizados: primero va al proveedor para obtener contenido fresco y calcular content_hash, luego busca en caché. Si hay hit (contenido no cambió), retorna caché. Si hay miss, guarda y retorna.
      - Crear `src/application/use_cases/read_full.py`:
        - Constructor recibe `provider: ProviderInterface` y `cache: CacheRepositoryInterface`
        - `execute(item_id, provider_name)`:
          1. **PRIMERO:** Llamar `provider.get_item(item_id, provider._config)` para obtener `ContextItem` con content_hash
          2. Buscar en caché con `cache.lookup(item_id, provider_name, item.content_hash, "read_full")`
          3. Si hay hit: retornar la entrada cacheada
          4. Si hay miss: construir `CacheEntry` con `CacheEntryBuilder`, llamar `cache.store(entry)` y retornar
      - _Ver `requirements.md`: Req. 3 — read_full (§1,2,3,4)_

    - [ ]* 9.2 Escribir unit tests para ReadFullUseCase
      > Tests con mocks de proveedor y caché para verificar el comportamiento en cache hit y miss. **IMPORTANTE:** Verificar que el flujo híbrido primero va al proveedor, luego busca en caché.
      - Archivo: `tests/unit/test_read_full_usecase.py`
      - Test cache hit: mock de `provider.get_item` retorna item con content_hash → mock de `cache.lookup` retorna CacheEntry → verificar que se retorna `from_cache=True`
      - Test cache miss: mock de `provider.get_item` retorna item → mock de `cache.lookup` retorna `None` → verificar que `cache.store` es llamado y se retorna `from_cache=False`
      - Test flujo: verificar que `provider.get_item` SIEMPRE es llamado (datos frescos), y `cache.lookup` se llama con el content_hash del item
      - _Ver `requirements.md`: Req. 3 — read_full (§3,4)_

  - [ ] 9.3 Implementar `ReadSummarizeUseCase`
    > Devuelve un resumen del ítem generado por el LLM. El flujo híbrido garantiza datos siempre actualizados: primero va al proveedor, calcula content_hash, luego busca en caché. Si hay hit (contenido no cambió), retorna caché sin llamar LLM.
    - Crear `src/application/services/read_summarize.py`:
      - Constructor recibe `provider`, `cache` y `summarized: SummarizeEngineInterface`
      - `execute(item_id, provider_name, max_tokens=500)`:
        1. Validar que `max_tokens` esté en el rango [1, 10000]; si no, lanzar `ValidationError` con mensaje descriptivo
        2. **PRIMERO:** Llamar `provider.get_item(item_id, provider._config)` para obtener `ContextItem` con content_hash
        3. Buscar en caché con `cache.lookup(item_id, provider_name, item.content_hash, "read_summarize", max_tokens=max_tokens)`
        4. Si hay hit: retornar la entrada cacheada
        5. Si hay miss: llamar `summarized.summarize(item.raw_content, max_tokens)` para generar el resumen
        6. Construir `CacheEntry` con el resumen y `metadata={"max_tokens": max_tokens}`, guardar en caché y retornar
    - _Ver `requirements.md`: Req. 4 — read_summarize (§1,2,3,4,5,6,7)_

  - [ ]* 9.4 Escribir property tests para ReadSummarizeUseCase
    > Verifica que la validación de `max_tokens` es robusta y que el flujo híbrido detecta cambios de contenido correctamente.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 5:** Para cualquier `max_tokens` fuera del rango [1, 10000], `execute()` siempre lanza `ValidationError`. Para cualquier valor dentro del rango, nunca lanza ese error.
    - **Propiedad 12:** Si el contenido cambia (nuevo content_hash), siempre hay cache miss y el LLM es llamado. Si el contenido no cambió (mismo content_hash), hay cache hit y el LLM no es llamado.
    - Comentario: `# Feature: contextforge, Propiedad 5: Rechazo de max_tokens fuera de rango`
    - _Ver `requirements.md`: Req. 4 — read_summarize (§7), Req. 6 — Caché (§2)_

  - [ ] 9.5 Implementar `ReadChunksUseCase`
    > Divide el contenido del ítem en fragmentos de máximo 500 tokens, respetando límites de oraciones. El flujo híbrido garantiza datos siempre actualizados: primero va al proveedor, luego busca en caché por content_hash. El cliente puede pedir todos los chunks o solo algunos por índice.
    > **Nota:** `ReadChunksUseCase` tiene la misma estructura que `ReadSummarizeUseCase` (`provider, cache, summarized`) pero con lógica distinta: usa `count_tokens()` directamente del engine.
    - Crear `src/application/services/read_chunks.py`:
      - Constructor recibe `provider`, `cache` y `summarized: SummarizeEngineInterface`
      - `execute(item_id, provider_name, chunk_indices=None)`:
        1. **PRIMERO:** Llamar `provider.get_item(item_id, provider._config)` para obtener `ContextItem` con content_hash
        2. Buscar en caché con `cache.lookup(item_id, provider_name, item.content_hash, "read_chunks")`
        3. Si hay hit: recuperar chunks de la caché
        4. Si hay miss: llamar `_split_into_chunks(item.raw_content)` para fragmentar
        5. Guardar cada chunk en caché individualmente
        6. Si `chunk_indices` no es `None`, llamar `_filter_by_indices(chunks, chunk_indices)`
        7. Retornar la lista de chunks
      - `_split_into_chunks(text)`: dividir usando regex `(?<=[.!?])\s+` para respetar límites de oración. Cada chunk debe tener ≤ 500 tokens (usar `llm.count_tokens()`). `chunk_index` empieza en 1. Actualizar `total_chunks` en todos los chunks al final.
      - `_filter_by_indices(chunks, indices)`: si algún índice está fuera del rango [1, total_chunks], lanzar `ValidationError` con mensaje que indique el rango válido
    - _Ver `requirements.md`: Req. 5 — read_chunks (§1,2,3,4,5,6,7,9)_

  - [ ]* 9.6 Escribir property tests para ReadChunksUseCase
    > Verifica las propiedades fundamentales de la fragmentación y el flujo híbrido: límite de tokens, cobertura completa del texto, selección correcta por índice, y detección de cambios de contenido.
    - Archivo: `tests/property/test_properties_chunks.py`
    - **Propiedad 6:** Para cualquier texto, ningún chunk supera 500 tokens.
    - **Propiedad 7:** La concatenación de todos los chunks contiene todo el contenido original (sin pérdida de texto).
    - **Propiedad 8:** Si se piden los índices [i, j], el resultado contiene exactamente esos chunks y ningún otro.
    - **Propiedad 9:** Si se pide un índice fuera del rango válido, siempre se lanza `ValidationError` con el rango correcto en el mensaje.
    - **Propiedad 10:** Ningún chunk corta una oración a la mitad (el texto de cada chunk termina en `.`, `!` o `?` o es el último chunk).
    - **Propiedad 11 (actualizada):** Si el content_hash del ítem cambia (contenido modificado en el proveedor), el flujo híbrido siempre detecta cache miss y regenera los chunks.
    - Comentario: `# Feature: contextforge, Propiedad 6: Chunks no exceden el límite de tokens`
    - _Ver `requirements.md`: Req. 5 — read_chunks (§2,4,7,9), Req. 6 — Caché (§3,5)_

- [ ] 10. Checkpoint — Verificar capa de dominio y aplicación
  > Pausa para verificar que todo lo construido hasta aquí funciona correctamente antes de continuar con la interfaz HTTP. Es más fácil corregir errores de lógica ahora que después de agregar FastAPI encima.
  - Ejecutar todos los tests: `pytest tests/unit/ tests/property/ -v`
  - Verificar que no hay errores de importación entre módulos
  - Preguntar al usuario si hay dudas o ajustes antes de continuar con la Interface Layer


- [ ] 11. Implementar Application Layer: ContextService (Facade)
  > El `ContextService` es la fachada que simplifica el acceso a los casos de uso desde los controllers. Valida que el proveedor solicitado esté configurado en la sesión antes de delegar al caso de uso correspondiente.

  - [ ] 11.1 Implementar `ContextService`
    > Sin esta fachada, cada controller tendría que instanciar el proveedor, verificar la sesión y crear el caso de uso. La fachada centraliza esa lógica.
    - Crear `src/application/services/context_service.py`:
      - Constructor recibe `cache: CacheRepositoryInterface` y `llm: LLMEngineInterface`
      - Tres métodos públicos: `read_full`, `read_summarize`, `read_chunks`
      - Cada método recibe `item_id`, `provider_name` y `session: SessionConfig` (más parámetros específicos)
      - Antes de delegar: verificar que `provider_name` está en `session.providers`. Si no, lanzar `SessionConfigError` con la lista de proveedores disponibles en la sesión
      - Si está: obtener `provider_config = session.providers[provider_name]`, instanciar el proveedor con `ProviderFactory.create(provider_name, provider_config)` y delegar al caso de uso correspondiente
    - _Ver `requirements.md`: Req. 3 — read_full (§1,5), Req. 4 — read_summarize (§1), Req. 5 — read_chunks (§1)_

  - [ ]* 11.2 Escribir unit tests para ContextService
    > Verifica que la fachada valida correctamente la sesión y delega al caso de uso correcto.
    - Archivo: `tests/unit/test_context_service.py`
    - Test `SessionConfigError`: llamar cualquier método con un `provider_name` que no está en `session.providers` → verificar que se lanza `SessionConfigError` con mensaje que incluye los proveedores disponibles
    - Test delegación `read_full`: verificar que se llama `ReadFullUseCase.execute()` con los parámetros correctos
    - Test delegación `read_summarize`: verificar que se llama `ReadSummarizeUseCase.execute()` con `max_tokens` correcto
    - Test delegación `read_chunks`: verificar que se llama `ReadChunksUseCase.execute()` con `chunk_indices` correcto
    - _Ver `requirements.md`: Req. 3 — read_full (§5), Req. 4 — read_summarize (§1), Req. 5 — read_chunks (§1)_

- [ ] 12. Implementar Interface Layer: Schemas y SessionManager
  > Los schemas Pydantic validan automáticamente el JSON que llega en las requests HTTP. El `SessionManager` guarda en memoria la configuración de cada sesión MCP activa.

  - [ ] 12.1 Implementar schemas Pydantic
    > Pydantic valida y parsea el JSON de entrada automáticamente. Si el cliente envía un campo con tipo incorrecto, FastAPI retorna 422 antes de que el código llegue al controller.
    - Crear `app/schemas/mcp_request.py` con los modelos de entrada:
      - `ProviderConfigSchema`: campos `token: str` y `base_url: str | None = None`
      - `SessionConfigSchema`: campo `providers: dict[str, ProviderConfigSchema]`
      - `ClientInfoSchema`: campo `config: SessionConfigSchema | None = None`
      - `InitializeParams`: campos `clientInfo: ClientInfoSchema | None = None` y `protocolVersion: str = "2025-03-26"`
      - `ToolCallParams`: campos `name: str` y `arguments: dict[str, Any] = {}`
      - `ToolCallRequest`: campos `jsonrpc: str = "2.0"`, `id: str | int | None = None`, `method: str` y `params: dict[str, Any] = {}`
    - Crear `app/schemas/mcp_response.py` con los modelos de salida:
      - `ToolCallResponse`: campos `content: str` y `from_cache: bool`
      - `ChunkItem`: campos `chunk_index: int`, `total_chunks: int`, `content: str` y `token_count: int`
      - `ChunksResponse`: campos `chunks: list[ChunkItem]` y `from_cache: bool`
    - Crear `app/schemas/errors.py`:
      - `ErrorResponse`: campo `message: str` con `json_schema_extra = {"example": {"message": "Descripción del error"}}`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§2), Req. 12 — Integración agentes AI (§1)_

  - [ ] 12.2 Implementar `SessionManager`
    > Guarda en memoria la configuración de cada sesión MCP. Cuando el cliente hace `initialize`, se guarda su config. Cuando hace `tools/call`, se recupera para saber qué proveedores tiene disponibles.
    - Crear `app/session.py`:
      - Clase `SessionManager` con `_sessions: dict[str, SessionConfig] = {}`
      - `store(session_id, config)`: validar antes de guardar:
        - Si `config.providers` está vacío → lanzar `SessionConfigError("La sesión debe tener al menos un proveedor")`
        - Si algún `token` está vacío → lanzar `SessionConfigError("El token del proveedor X no puede estar vacío")`
        - Si es válida: guardar en `_sessions[session_id] = config`
      - `get(session_id)`: retornar `_sessions[session_id]`. Si no existe → lanzar `SessionConfigError("Sesión no encontrada. Llama a initialize primero.")`
      - `delete(session_id)`: eliminar silenciosamente si existe, ignorar si no existe
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§2,3,4,5)_

  - [ ]* 12.3 Escribir property tests para SessionManager
    > Verifica que la validación de sesiones es robusta para cualquier combinación de inputs inválidos.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 1:** Para cualquier `ProviderConfig` con `token` vacío o `base_url` con formato inválido, `store()` siempre lanza `SessionConfigError`.
    - **Propiedad 19:** Para cualquier `SessionConfig` con `providers` vacío, `store()` siempre lanza `SessionConfigError` con un mensaje descriptivo.
    - Comentario: `# Feature: contextforge, Propiedad 1: Validación de campos faltantes en ProviderConfig`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§4,5)_

- [ ] 13. Implementar Interface Layer: Controllers y Exception Handlers
  > Los controllers son los puntos de entrada HTTP. Reciben la request, la parsean con los schemas Pydantic, delegan al `ContextService` y retornan la respuesta. Los exception handlers capturan errores de dominio y los convierten en respuestas HTTP con el código correcto.

  - [ ] 13.1 Implementar `ApplicationController` base
    > Clase base que todos los controllers heredan. Recibe un `APIRouter` y lo guarda en `self.router` para que los controllers registren sus endpoints en él.
    - Crear `app/controllers/application_controller.py`:
      - Clase `ApplicationController` con constructor `__init__(self, router: APIRouter)` que guarda `self.router = router`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§1)_

  - [ ] 13.2 Implementar exception handlers globales
    > En lugar de manejar errores en cada endpoint, los handlers globales capturan las excepciones de dominio y retornan la respuesta HTTP correcta automáticamente. `main.py` los registra con `app.add_exception_handler()`.
    - Crear `app/exceptions/exception_handler.py`:
      - Handler async para cada excepción: `session_config_error_handler` → 400, `item_not_found_handler` → 404, `authentication_error_handler` → 401, `validation_error_handler` → 422, `provider_not_registered_handler` → 422, `generic_contextforge_handler` → 422
      - Cada handler retorna `JSONResponse(status_code=X, content={"message": str(exc)})`
      - Exportar `exception_handlers: dict = {SessionConfigError: handler, ...}` para que `main.py` lo itere
    - _Ver `requirements.md`: Req. 3 — read_full (§5,6,7), Req. 4 — read_summarize (§7), Req. 5 — read_chunks (§7)_

  - [ ] 13.3 Implementar `HealthController`
    > Endpoint simple para verificar que el servidor está vivo. Útil para Docker healthchecks y monitoreo.
    - Crear `app/controllers/health_controller.py`:
      - Clase `HealthController(ApplicationController)`
      - En `__init__`: registrar `@self.router.get("/health")` que retorna `{"status": "ok"}`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§1)_

  - [ ] 13.4 Implementar `MCPController`
    > El controller principal. Recibe todas las requests MCP en un único endpoint POST y las despacha según el campo `method` del body JSON.
    - Crear `app/controllers/mcp_controller.py`:
      - Clase `MCPController(ApplicationController)` con constructor que recibe `router`, `context_service` y `session_manager`
      - Registrar `POST /` que despacha según `request.method`:
        - `"initialize"` → `_handle_initialize`: parsear `params.clientInfo.config` como `SessionConfig`, llamar `session_manager.store(session_id, config)`, retornar respuesta MCP con `protocolVersion`, `capabilities: {}` y `serverInfo: {"name": "contextforge", "version": "1.0.0"}`
        - `"tools/list"` → `_handle_tools_list`: retornar lista de las tres herramientas (`read_full`, `read_summarize`, `read_chunks`) con descripciones que guíen al agente a elegir la correcta según su necesidad
        - `"tools/call"` → `_handle_tool_call`: obtener sesión con `session_manager.get(session_id)`, despachar a `context_service.read_full/read_summarize/read_chunks` según `params.name`, serializar y retornar la respuesta
        - Cualquier otro método → retornar `JSONResponse({"message": "Método no soportado"}, status_code=400)`
      - Registrar `GET /` que retorna `{"message": "SSE endpoint activo"}` (stub para compatibilidad con spec MCP 2025-03-26)
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§1,2,3,6), Req. 3 — read_full (§1), Req. 4 — read_summarize (§1), Req. 5 — read_chunks (§1), Req. 12 — Integración agentes AI (§1,3,4)_

  - [ ]* 13.5 Escribir property tests para validaciones del MCPController
    > Verifica que el controller rechaza correctamente inputs inválidos y que las respuestas contienen solo el contexto solicitado.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 2:** Para cualquier `base_url` con formato inválido (sin `http://` o `https://`, con espacios, etc.), el sistema retorna error antes de intentar conectarse al proveedor.
    - **Propiedad 17:** La respuesta de `tools/call` contiene exactamente el contenido solicitado: `read_full` retorna el texto completo, `read_summarize` retorna solo el resumen, `read_chunks` retorna solo los chunks pedidos.
    - Comentario: `# Feature: contextforge, Propiedad 2: Rechazo de URL con formato inválido`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§5), Req. 12 — Integración agentes AI (§3)_


- [ ] 14. Implementar `settings.py` y `main.py`
  > El punto de entrada de la aplicación. `settings.py` carga y valida las variables de entorno al arrancar. `main.py` crea la app FastAPI, conecta todos los componentes y registra las rutas.

  - [ ] 14.1 Implementar `settings.py`
    > Usar `pydantic-settings` para cargar variables de entorno con validación automática de tipos. Si falta `LLM_API_KEY`, el servidor no debe arrancar.
    - Crear `settings.py` en la raíz del proyecto:
      - Clase `Settings(BaseSettings)` con campos:
        - `LLM_ENGINE: str = "gemini"` (motor LLM a usar)
        - `LLM_API_KEY: str` (requerida, sin default)
        - `CHROMA_HOST: str = "chromadb"` (nombre del servicio en docker-compose)
        - `CHROMA_PORT: int = 8000` (puerto interno de ChromaDB)
        - `MCP_PORT: int = 8999` (puerto de la app)
        - `LOG_LEVEL: str = "INFO"`
      - Método `get_llm_config()` que retorna `LLMConfig(engine_type=self.LLM_ENGINE, api_key=self.LLM_API_KEY)`
      - Al final del archivo: `settings = Settings()`. Si `LLM_API_KEY` está vacía, loguear el error y llamar `sys.exit(1)`
    - _Ver `requirements.md`: Req. 2 — Config LLM (§1,3,4,5), Req. 11 — Docker (§2,6)_

  - [ ]* 14.2 Escribir property test para settings
    > Verifica que el servidor falla al arrancar si faltan variables de entorno requeridas.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 15:** Para cualquier combinación de variables de entorno donde `LLM_API_KEY` está ausente o vacía, la inicialización de `Settings` lanza un error (o llama `sys.exit(1)`). Con `LLM_API_KEY` presente, siempre inicializa correctamente.
    - Usar `unittest.mock.patch.dict(os.environ, {...})` para simular variables de entorno
    - Comentario: `# Feature: contextforge, Propiedad 15: Fallo al iniciar con variables de entorno requeridas faltantes`
    - _Valida: Requisito 2.4_

  - [ ] 14.3 Implementar `main.py` y `config/routes.py`
    > `main.py` es el punto de entrada que conecta todo. `config/routes.py` monta los controllers en la app FastAPI.
    - Crear `config/routes.py`:
      - Clase `Routes` con constructor `__init__(self, app: FastAPI, **deps)` que guarda `self._app` y `self._deps`
      - Método `register()`: crear un `APIRouter`, instanciar `MCPController(router, **deps)` y `HealthController(router)`, montar con `app.include_router(..., prefix="/mcp")` y `app.include_router(...)`
    - Crear `main.py`:
      - Instanciar `FastAPI(title="ContextForge MCP Server", version="1.0.0")`
      - Iterar `exception_handlers.items()` y registrar cada uno con `app.add_exception_handler(exc_class, handler)`
      - Importar `src.infrastructure.providers` y `src.infrastructure.llm` (esto activa los registros en los factories)
      - Inicializar: `cache = ChromaCacheRepository(...)`, `llm = LLMFactory.create(...)`, `context_service = ContextService(...)`, `session_manager = SessionManager()`
      - Llamar `Routes(app, context_service=context_service, session_manager=session_manager).register()`
    - _Ver `requirements.md`: Req. 1 — Inicialización MCP (§1), Req. 2 — Config LLM (§2), Req. 10 — ChromaDB (§3), Req. 11 — Docker (§3)_

- [ ] 15. Implementar property tests de caché
  > Tests que verifican el comportamiento del sistema de caché de extremo a extremo: que los datos se guardan y recuperan correctamente, y que la caché se invalida cuando el contenido cambia.

  - [ ]* 15.1 Escribir property tests para comportamiento de caché
    > Verifica las propiedades fundamentales del sistema de caché usando mocks de ChromaDB.
    - Archivo: `tests/property/test_properties_cache.py`
    - **Propiedad 3:** Para cualquier `CacheEntry` almacenada con `store()`, una llamada inmediata a `lookup()` con los mismos parámetros siempre retorna la misma entrada con `from_cache=True` (round-trip).
    - **Propiedad 11:** Si el `content_hash` de un ítem cambia (el contenido fue modificado en el proveedor), `lookup()` con el nuevo hash retorna `None` (cache miss), forzando la regeneración del contenido.
    - Comentario: `# Feature: contextforge, Propiedad 3: Round-trip de caché por herramienta`
    - _Ver `requirements.md`: Req. 3 — read_full (§4), Req. 4 — read_summarize (§6), Req. 5 — read_chunks (§6), Req. 6 — Caché (§3,5)_

- [ ] 16. Checkpoint final — Integración completa
  > Verificación final de que todo el sistema funciona de extremo a extremo: tests, servidor y Docker.
  - Ejecutar todos los tests: `pytest tests/ -v` y verificar que todos pasan
  - Verificar que el servidor arranca correctamente: `uvicorn main:app --port 8999`
  - Verificar que `GET /health` retorna `{"status": "ok"}`
  - Verificar que `docker-compose up` levanta ambos servicios (`contextforge` y `chromadb`) sin errores
  - Preguntar al usuario si hay dudas o ajustes antes de cerrar el spec
