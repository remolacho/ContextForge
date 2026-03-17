# Plan de Implementación: ContextForge

## Visión General

Implementación incremental de ContextForge siguiendo Clean Architecture: primero el dominio, luego infraestructura, después la capa de aplicación y finalmente la interfaz HTTP/MCP. Cada tarea construye sobre la anterior y termina con la integración completa.

> **Para dev junior:** Lee el `design.md` antes de empezar. Cada tarea indica el archivo a crear, qué debe contener y por qué existe. Las tareas marcadas con `*` son opcionales (property tests) pero muy recomendadas.

## Tareas

- [ ] 1. Configurar estructura del proyecto y dependencias
  > Prepara el esqueleto del proyecto: archivos de configuración, dependencias Python, Docker y todos los directorios vacíos. Sin esto, nada más puede ejecutarse. Es la base sobre la que se construye todo.
  - Crear `pyproject.toml` con dependencias: `fastapi`, `uvicorn`, `pydantic-settings`, `chromadb`, `langchain`, `langchain-google-genai`, `langchain-core`, `requests`, `hypothesis`, `pytest`, `pytest-asyncio`
  - Crear `requirements.txt` generado desde `pyproject.toml` (ejecutar `pip-compile` o exportar manualmente)
  - Crear `.env.example` documentando todas las variables: `LLM_ENGINE`, `LLM_API_KEY`, `CHROMA_HOST`, `CHROMA_PORT`, `MCP_PORT`, `LOG_LEVEL`
  - Crear `Dockerfile` basado en `python:3.12-slim` con `PYTHONPATH=/app` para que los imports funcionen desde la raíz
  - Crear `docker-compose.yml` con dos servicios: `contextforge` (puerto 8999) y `chromadb` (puerto 9000→8000), conectados en red `contextforge-net`, con volumen `chroma-data` para persistencia
  - Crear todos los directorios y archivos `__init__.py` vacíos según la estructura del `design.md` (sin `__init__.py` Python no reconoce los módulos)
  - _Requisitos: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 2. Implementar Domain Layer
  > El dominio es el núcleo del sistema: define qué datos existen, qué contratos deben cumplir los componentes y qué errores pueden ocurrir. No depende de ninguna librería externa. Si el dominio está bien definido, el resto del código es predecible.

  - [ ] 2.1 Crear entidades de dominio
    > Las entidades son los objetos de datos que viajan por todo el sistema. Usar `@dataclass` de Python para definirlas de forma limpia sin boilerplate.
    - Implementar `src/domain/entities.py` con las siguientes dataclasses:
      - `ProviderConfig`: guarda `token` y `base_url` opcional de un proveedor (ej. YouTrack)
      - `SessionConfig`: contiene un dict `providers` donde la clave es el nombre del proveedor y el valor es su `ProviderConfig`
      - `LLMConfig`: guarda `engine_type` (ej. "gemini") y `api_key` para el motor LLM
      - `ContextItem`: representa un ítem recuperado del proveedor con `item_id`, `title`, `description`, `comments`, `custom_fields`, `raw_content` (texto concatenado) y `content_hash` (SHA-256)
      - `Chunk`: representa un fragmento de texto con `chunk_index` (empieza en 1), `total_chunks`, `content` y `token_count`
      - `CacheEntry`: representa una entrada en caché con `item_id`, `provider_name`, `content_hash`, `tool`, `content`, `metadata` y `from_cache: bool`
    - _Requisitos: 1.2, 3.1, 4.1, 5.2_

  - [ ] 2.2 Crear interfaces (ports) de dominio
    > Las interfaces definen los contratos que deben cumplir las implementaciones concretas. Permiten que los casos de uso no dependan de ChromaDB, YouTrack o Gemini directamente, sino de abstracciones. Esto facilita testear con mocks y cambiar implementaciones sin tocar la lógica de negocio.
    - Implementar `src/domain/interfaces.py` con tres ABCs (clases abstractas):
      - `ProviderInterface`: contrato para proveedores de datos. Métodos: `get_item(item_id, config) → ContextItem` y `validate_config(config) → bool`
      - `CacheRepositoryInterface`: contrato para el repositorio de caché. Métodos: `lookup(item_id, provider_name, content_hash, tool, **kwargs) → CacheEntry | None`, `store(entry)` e `invalidate(item_id, provider_name, tool)`
      - `LLMEngineInterface`: contrato para el motor LLM. Métodos: `summarize(content, max_tokens) → str`, `count_tokens(text) → int` y `get_embeddings(text) → list[float]`
    - _Requisitos: 7.5, 8.4_

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
    - _Requisitos: 1.4, 3.5, 3.6, 3.7, 4.7, 5.7, 7.3, 8.3_


- [ ] 3. Implementar Infrastructure Layer: Builders
  > Los builders construyen objetos complejos paso a paso usando una API fluida (encadenamiento de métodos). Evitan constructores con muchos parámetros y centralizan la lógica de construcción (ej. calcular el hash SHA-256 siempre en el mismo lugar).

  - [ ] 3.1 Implementar `ContextItemBuilder`
    > Este builder toma la respuesta JSON cruda de YouTrack y la convierte en un `ContextItem` limpio. Centraliza el cálculo del `content_hash` para que siempre sea consistente.
    - Crear `src/infrastructure/builders/context_item.py` con métodos fluidos:
      - `set_item_id(item_id)`: guarda el ID del ítem
      - `set_provider_name(name)`: guarda el nombre del proveedor
      - `from_youtrack_response(data: dict)`: extrae `summary`, `description`, `comments` y `customFields` del JSON de YouTrack
      - `build()`: concatena título + descripción + comentarios en `raw_content`, calcula `content_hash` como SHA-256 de `raw_content` y retorna el `ContextItem`
    - _Requisitos: 9.3, 6.1_

  - [ ]* 3.2 Escribir property test para ContextItemBuilder
    > Verifica que el hash SHA-256 siempre es el mismo para el mismo contenido (determinismo) y diferente para contenido diferente.
    - Archivo: `tests/property/test_properties_providers.py`
    - **Propiedad 20:** Para cualquier combinación de título, descripción y comentarios, `build()` siempre produce el mismo `content_hash` (SHA-256 determinista). Si cambia cualquier campo, el hash cambia.
    - Usar `@given(st.text(), st.text(), st.lists(st.text()))` de hypothesis con `@settings(max_examples=100)`
    - Comentario en el test: `# Feature: contextforge, Propiedad 20: ContextItemBuilder produce content_hash SHA-256 consistente`
    - _Valida: Requisito 6.1_

  - [ ] 3.3 Implementar `CacheEntryBuilder`
    > Construye una `CacheEntry` completa con todos sus metadatos de forma legible. Evita crear el objeto con un constructor de 7 parámetros.
    - Crear `src/infrastructure/builders/cache_entry.py` con métodos fluidos:
      - `for_item(item: ContextItem)`: copia `item_id`, `provider_name` y `content_hash` del ítem
      - `with_tool(tool: str)`: establece la herramienta (`"read_full"`, `"read_summarize"`, `"read_chunks"`)
      - `with_content(content: str)`: establece el contenido a cachear
      - `with_metadata(**kwargs)`: agrega metadatos adicionales (ej. `timestamp`, `max_tokens`)
      - `build()`: retorna el `CacheEntry` con `from_cache=False`
    - _Requisitos: 3.3, 4.5, 5.5_

- [ ] 4. Implementar Infrastructure Layer: Factories
  > Los factories crean instancias de proveedores y motores LLM por nombre, sin que el código que los usa sepa qué clase concreta se instancia. Esto permite agregar nuevos proveedores o motores sin modificar el código existente (principio Open/Closed).

  - [ ] 4.1 Implementar `ProviderFactory`
    > Registro central de proveedores. Cuando el cliente pide `"youtrack"`, el factory sabe qué clase instanciar y a qué categoría pertenece (`"task"`). Agregar Jira en el futuro solo requiere registrarlo aquí.
    - Crear `src/infrastructure/providers/factory.py`:
      - Dataclass `ProviderRegistration` con campos `category: str` y `cls: type[ProviderInterface]`
      - Clase `ProviderFactory` con atributo de clase `_registry: dict[str, ProviderRegistration] = {}`
      - `register(provider_name, category, provider_cls)`: agrega al registro. Ejemplo: `register("youtrack", "task", YouTrackProvider)`
      - `create(provider_name, config)`: busca en el registro e instancia el proveedor. Si no existe, lanza `ProviderNotRegisteredError` con la lista de disponibles
      - `get_category(provider_name)`: retorna la categoría (`"task"`, `"git"`, `"file"`) del proveedor registrado
    - _Requisitos: 7.1, 7.2, 7.3, 7.4_

  - [ ]* 4.2 Escribir property test para ProviderFactory
    > Verifica que el factory siempre instancia la clase correcta y retorna la categoría correcta para cualquier proveedor registrado.
    - Archivo: `tests/property/test_properties_providers.py`
    - **Propiedad 16:** Para cualquier proveedor registrado, `create()` retorna una instancia de la clase correcta y `get_category()` retorna la categoría registrada. Para nombres no registrados, siempre lanza `ProviderNotRegisteredError`.
    - Comentario: `# Feature: contextforge, Propiedad 16: ProviderFactory instancia el proveedor correcto según nombre e infiere su categoría`
    - _Valida: Requisito 7.3_

  - [ ] 4.3 Implementar `LLMFactory`
    > Igual que `ProviderFactory` pero para motores LLM. Permite cambiar de Gemini a OpenAI solo cambiando la variable de entorno `LLM_ENGINE`.
    - Crear `src/infrastructure/llm/factory.py`:
      - Clase `LLMFactory` con `_registry: dict[str, type[LLMEngineInterface]] = {}`
      - `register(engine_type, cls_)`: registra un motor. Ejemplo: `register("gemini", GeminiLLMEngine)`
      - `create(engine_type, config)`: instancia el motor. Si no existe, lanza `LLMEngineNotRegisteredError` con la lista de disponibles
    - _Requisitos: 8.1, 8.2, 8.3, 8.7_

  - [ ]* 4.4 Escribir property test para LLMFactory
    > Verifica que el factory siempre instancia el motor correcto y falla con error descriptivo para motores no registrados.
    - Archivo: `tests/property/test_properties_providers.py`
    - **Propiedad 18:** Para cualquier motor registrado, `create()` retorna una instancia de la clase correcta. Para tipos no registrados, siempre lanza `LLMEngineNotRegisteredError`.
    - Comentario: `# Feature: contextforge, Propiedad 18: LLMFactory instancia el motor correcto según LLM_ENGINE`
    - _Valida: Requisito 8.3_


- [ ] 5. Implementar Infrastructure Layer: Proveedores
  > Los proveedores son los adaptadores que saben cómo hablar con sistemas externos (YouTrack, Jira, etc.). Implementan `ProviderInterface` para que el resto del sistema no sepa ni le importe con qué API externa se está comunicando.

  - [ ] 5.1 Implementar `YouTrackProvider`
    > El único proveedor funcional del MVP. Hace una llamada HTTP a la API de YouTrack, maneja los errores de autenticación y construye el `ContextItem` usando el builder.
    - Crear `src/infrastructure/providers/task/youtrack.py` implementando `ProviderInterface`:
      - Constructor recibe `config: ProviderConfig` y lo guarda en `self._config`
      - `get_item(item_id, config)`: hace GET a `{config.base_url}/api/issues/{item_id}?fields=id,summary,description,comments(text),customFields(name,value)` con header `Authorization: Bearer {config.token}`
      - Mapeo de errores HTTP: 401/403 → lanzar `AuthenticationError`, 404 → `ItemNotFoundError`, 5xx → `ProviderServerError`
      - Usar `ContextItemBuilder` para construir el `ContextItem` desde el JSON de respuesta
      - `validate_config(config)`: retorna `True` si `token` no está vacío y `base_url` es una URL válida
    - _Requisitos: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_

  - [ ]* 5.2 Escribir property tests para YouTrackProvider
    > Verifica que el header de autenticación siempre está presente y que todos los campos del JSON de YouTrack se extraen correctamente.
    - Archivo: `tests/property/test_properties_providers.py`
    - **Propiedad 13:** Para cualquier token válido, todas las solicitudes HTTP incluyen el header `Authorization: Bearer {token}`. Usar `unittest.mock.patch` para interceptar las llamadas HTTP.
    - **Propiedad 14:** Para cualquier respuesta JSON válida de YouTrack, `get_item()` extrae correctamente `summary`, `description`, `comments` y `customFields` sin perder datos.
    - Comentario: `# Feature: contextforge, Propiedad 13: Header de autenticación en todas las solicitudes al proveedor`
    - _Valida: Requisitos 9.2, 9.3_

  - [ ] 5.3 Crear stubs de proveedores futuros
    > Crear los archivos vacíos ahora establece la estructura para escalar. Un stub implementa la interfaz pero lanza `NotImplementedError`, dejando claro que aún no está implementado.
    - Crear `src/infrastructure/providers/task/jira.py`: clase `JiraProvider(ProviderInterface)` que lanza `NotImplementedError("JiraProvider no implementado aún")` en todos sus métodos
    - Crear `src/infrastructure/providers/git/github.py`: `GitHubProvider` stub igual
    - Crear `src/infrastructure/providers/git/gitlab.py`: `GitLabProvider` stub igual
    - Crear `src/infrastructure/providers/file/pdf.py`: `PDFProvider` stub igual
    - Crear `src/infrastructure/providers/file/markdown.py`: `MarkdownProvider` stub igual
    - _Requisitos: 7.4, 7.7_

  - [ ] 5.4 Registrar proveedores en `__init__.py`
    > Al importar `src.infrastructure.providers`, Python ejecuta este `__init__.py` que registra todos los proveedores en el factory. Así `main.py` solo necesita hacer el import para activar el registro.
    - Implementar `src/infrastructure/providers/__init__.py`:
      - Importar `ProviderFactory`, `YouTrackProvider` y `JiraProvider`
      - Registrar: `ProviderFactory.register("youtrack", "task", YouTrackProvider)` y `ProviderFactory.register("jira", "task", JiraProvider)`
      - Dejar comentados los registros de git y file con un comentario `# Descomentar cuando se implemente`
    - _Requisitos: 7.1, 7.4_

- [ ] 6. Implementar Infrastructure Layer: LLM
  > Integra LangChain con Gemini para generar resúmenes. Usa el patrón LCEL (LangChain Expression Language) que encadena prompt → modelo → parser de forma declarativa y legible.

  - [ ] 6.1 Implementar prompts LangChain
    > Centralizar el prompt en un archivo dedicado evita duplicación y facilita ajustarlo sin tocar la lógica del engine. Usar `ChatPromptTemplate.from_messages` con roles `system`/`human` es la práctica recomendada de LangChain.
    - Crear `src/infrastructure/llm/prompts.py`:
      - Importar `ChatPromptTemplate` de `langchain_core.prompts`
      - Definir constante `SUMMARIZE_PROMPT = ChatPromptTemplate.from_messages([("system", "..."), ("human", "...")])` con variables `{max_tokens}` y `{content}`
      - El mensaje `system` debe instruir al modelo a resumir en máximo `{max_tokens}` tokens
      - El mensaje `human` debe contener el `{content}` a resumir
    - _Requisitos: 8.6_

  - [ ] 6.2 Implementar `GeminiLLMEngine`
    > Implementación concreta del motor LLM usando Gemini. Construye la chain LCEL que conecta el prompt con el modelo y el parser de salida.
    - Crear `src/infrastructure/llm/gemini.py` implementando `LLMEngineInterface`:
      - Constructor recibe `config: LLMConfig` e inicializa:
        - `self._llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=config.api_key)`
        - `self._embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=config.api_key)`
        - `self._chain = SUMMARIZE_PROMPT | self._llm | StrOutputParser()` (chain LCEL)
      - `summarize(content, max_tokens)`: invoca `self._chain.invoke({"content": content, "max_tokens": max_tokens})`; capturar cualquier excepción y relanzar como `LLMError`
      - `count_tokens(text)`: retorna `self._llm.get_num_tokens(text)`
      - `get_embeddings(text)`: retorna `self._embeddings.embed_query(text)`
    - _Requisitos: 8.5, 8.6, 8.7_

  - [ ] 6.3 Crear stub `OpenAILLMEngine` y registrar motores
    > El stub de OpenAI establece la estructura para cuando se quiera agregar ese motor. El `__init__.py` activa el registro al importar el módulo.
    - Crear `src/infrastructure/llm/openai.py`: clase `OpenAILLMEngine(LLMEngineInterface)` que lanza `NotImplementedError` en todos sus métodos
    - Implementar `src/infrastructure/llm/__init__.py`:
      - Importar `LLMFactory`, `GeminiLLMEngine`, `OpenAILLMEngine`
      - Registrar: `LLMFactory.register("gemini", GeminiLLMEngine)` y `LLMFactory.register("openai", OpenAILLMEngine)`
    - _Requisitos: 8.1, 8.7_


- [ ] 7. Implementar Infrastructure Layer: ChromaCacheRepository
  > Implementa el repositorio de caché usando ChromaDB. Cada entrada se identifica por la combinación `item_id + provider_name + content_hash + tool`. Si el contenido del ítem cambia (nuevo `content_hash`), la caché no hace match y se regenera.

  - [ ] 7.1 Implementar `ChromaCacheRepository`
    > ChromaDB es una base de datos vectorial. Aquí la usamos principalmente como almacén de documentos con filtros por metadatos, no tanto por similitud semántica.
    - Crear `src/infrastructure/cache/chroma.py` implementando `CacheRepositoryInterface`:
      - Constructor: conectar con `chromadb.HttpClient(host=host, port=port)` y obtener/crear colección `contextforge_cache` con `get_or_create_collection()`
      - `lookup(item_id, provider_name, content_hash, tool, **kwargs)`: consultar la colección filtrando por metadatos `{"item_id": ..., "provider_name": ..., "content_hash": ..., "tool": ...}` más `max_tokens` si está en `kwargs`. Si hay resultado, retornar `CacheEntry` con `from_cache=True`. Si no, retornar `None`.
      - `store(entry)`: llamar `upsert()` con el documento, metadatos y un ID único generado por `_build_doc_id(entry)`
      - `invalidate(item_id, provider_name, tool)`: eliminar todas las entradas que coincidan con esos tres campos usando `delete(where={...})`
      - Función auxiliar `_build_doc_id(entry)`: construir un ID único como `f"{entry.item_id}:{entry.provider_name}:{entry.tool}:{entry.content_hash}"` (agregar `max_tokens` si aplica)
    - _Requisitos: 10.1, 10.2, 10.4, 6.1, 6.2_

  - [ ]* 7.2 Escribir unit tests para ChromaCacheRepository
    > Tests unitarios con mock de ChromaDB para verificar que los métodos llaman a la API de ChromaDB con los parámetros correctos.
    - Archivo: `tests/unit/test_chroma_cache.py`
    - Test `lookup` con cache hit: mock retorna un documento → verificar que se retorna `CacheEntry` con `from_cache=True`
    - Test `lookup` con cache miss: mock retorna lista vacía → verificar que se retorna `None`
    - Test `store`: verificar que `upsert` es llamado con los metadatos correctos (todos los campos de la `CacheEntry`)
    - Test `invalidate`: verificar que `delete` es llamado con el filtro `{"item_id": ..., "provider_name": ..., "tool": ...}`
    - _Requisitos: 10.2, 6.1_

- [ ] 8. Implementar Application Layer: Casos de Uso
  > Los casos de uso son el corazón de la lógica de negocio. Orquestan el flujo: obtener ítem del proveedor → verificar caché → procesar si es necesario → guardar en caché → retornar resultado. No saben nada de FastAPI, ChromaDB ni Gemini; solo hablan con interfaces.

  - [ ] 8.1 Implementar `ReadFullUseCase`
    > Devuelve el texto completo del ítem. Si ya está en caché con el mismo hash, lo retorna directamente sin llamar al proveedor.
    - Crear `src/application/use_cases/read_full.py`:
      - Constructor recibe `provider: ProviderInterface` y `cache: CacheRepositoryInterface`
      - `execute(item_id, provider_name)`:
        1. Llamar `provider.get_item(item_id, provider._config)` para obtener el `ContextItem`
        2. Llamar `cache.lookup(item_id, provider_name, item.content_hash, "read_full")`
        3. Si hay hit: retornar la entrada cacheada
        4. Si hay miss: construir `CacheEntry` con `CacheEntryBuilder`, llamar `cache.store(entry)` y retornar la entrada con `from_cache=False`
    - _Requisitos: 3.1, 3.2, 3.3, 3.4_

  - [ ]* 8.2 Escribir unit tests para ReadFullUseCase
    > Tests con mocks de proveedor y caché para verificar el comportamiento en cache hit y miss.
    - Archivo: `tests/unit/test_read_full_usecase.py`
    - Test cache hit: mock de `cache.lookup` retorna una `CacheEntry` → verificar que `provider.get_item` NO es llamado y se retorna `from_cache=True`
    - Test cache miss: mock de `cache.lookup` retorna `None` → verificar que `provider.get_item` SÍ es llamado, `cache.store` es llamado y se retorna `from_cache=False`
    - _Requisitos: 3.3, 3.4_

  - [ ] 8.3 Implementar `ReadSummarizeUseCase`
    > Devuelve un resumen del ítem generado por el LLM. El `max_tokens` forma parte de la clave de caché, por lo que un resumen de 200 tokens y uno de 500 tokens se cachean por separado.
    - Crear `src/application/use_cases/read_summarize.py`:
      - Constructor recibe `provider`, `cache` y `llm: LLMEngineInterface`
      - `execute(item_id, provider_name, max_tokens=500)`:
        1. Validar que `max_tokens` esté en el rango [1, 10000]; si no, lanzar `ValidationError` con mensaje descriptivo
        2. Obtener el ítem del proveedor
        3. Verificar caché incluyendo `max_tokens` como parámetro extra en `lookup(..., max_tokens=max_tokens)`
        4. Si hay miss: llamar `llm.summarize(item.raw_content, max_tokens)` para generar el resumen
        5. Construir `CacheEntry` con el resumen y `metadata={"max_tokens": max_tokens}`, guardar en caché y retornar
    - _Requisitos: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [ ]* 8.4 Escribir property tests para ReadSummarizeUseCase
    > Verifica que la validación de `max_tokens` es robusta y que el caché diferencia correctamente por valor de `max_tokens`.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 5:** Para cualquier `max_tokens` fuera del rango [1, 10000], `execute()` siempre lanza `ValidationError`. Para cualquier valor dentro del rango, nunca lanza ese error.
    - **Propiedad 12:** Si se llama con `max_tokens=A` y luego con `max_tokens=B` (A ≠ B), la segunda llamada siempre produce un cache miss (el LLM es llamado de nuevo).
    - Comentario: `# Feature: contextforge, Propiedad 5: Rechazo de max_tokens fuera de rango`
    - _Valida: Requisitos 4.7, 6.2_

  - [ ] 8.5 Implementar `ReadChunksUseCase`
    > Divide el texto del ítem en fragmentos de máximo 500 tokens, respetando límites de oraciones. El cliente puede pedir todos los chunks o solo algunos por índice.
    - Crear `src/application/use_cases/read_chunks.py`:
      - Constructor recibe `provider`, `cache` y `llm`
      - `execute(item_id, provider_name, chunk_indices=None)`:
        1. Obtener el ítem del proveedor
        2. Verificar caché con `tool="read_chunks"`
        3. Si hay miss: llamar `_split_into_chunks(item.raw_content)` para fragmentar
        4. Guardar cada chunk en caché individualmente
        5. Si `chunk_indices` no es `None`, llamar `_filter_by_indices(chunks, chunk_indices)`
        6. Retornar la lista de chunks
      - `_split_into_chunks(text)`: dividir usando regex `(?<=[.!?])\s+` para respetar límites de oración. Cada chunk debe tener ≤ 500 tokens (usar `llm.count_tokens()`). `chunk_index` empieza en 1. Actualizar `total_chunks` en todos los chunks al final.
      - `_filter_by_indices(chunks, indices)`: si algún índice está fuera del rango [1, total_chunks], lanzar `ValidationError` con mensaje que indique el rango válido
    - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.9_

  - [ ]* 8.6 Escribir property tests para ReadChunksUseCase
    > Verifica las propiedades fundamentales de la fragmentación: límite de tokens, cobertura completa del texto y selección correcta por índice.
    - Archivo: `tests/property/test_properties_chunks.py`
    - **Propiedad 6:** Para cualquier texto, ningún chunk supera 500 tokens.
    - **Propiedad 7:** La concatenación de todos los chunks contiene todo el contenido original (sin pérdida de texto).
    - **Propiedad 8:** Si se piden los índices [i, j], el resultado contiene exactamente esos chunks y ningún otro.
    - **Propiedad 9:** Si se pide un índice fuera del rango válido, siempre se lanza `ValidationError` con el rango correcto en el mensaje.
    - **Propiedad 10:** Ningún chunk corta una oración a la mitad (el texto de cada chunk termina en `.`, `!` o `?` o es el último chunk).
    - Comentario: `# Feature: contextforge, Propiedad 6: Chunks no exceden el límite de tokens`
    - _Valida: Requisitos 5.2, 5.4, 5.7, 5.9_

- [ ] 9. Checkpoint — Verificar capa de dominio y aplicación
  > Pausa para verificar que todo lo construido hasta aquí funciona correctamente antes de continuar con la interfaz HTTP. Es más fácil corregir errores de lógica ahora que después de agregar FastAPI encima.
  - Ejecutar todos los tests: `pytest tests/unit/ tests/property/ -v`
  - Verificar que no hay errores de importación entre módulos
  - Preguntar al usuario si hay dudas o ajustes antes de continuar con la Interface Layer


- [ ] 10. Implementar Application Layer: ContextService (Facade)
  > El `ContextService` es la fachada que simplifica el acceso a los casos de uso desde los controllers. Valida que el proveedor solicitado esté configurado en la sesión antes de delegar al caso de uso correspondiente.

  - [ ] 10.1 Implementar `ContextService`
    > Sin esta fachada, cada controller tendría que instanciar el proveedor, verificar la sesión y crear el caso de uso. La fachada centraliza esa lógica.
    - Crear `src/application/services/context_service.py`:
      - Constructor recibe `cache: CacheRepositoryInterface` y `llm: LLMEngineInterface`
      - Tres métodos públicos: `read_full`, `read_summarize`, `read_chunks`
      - Cada método recibe `item_id`, `provider_name` y `session: SessionConfig` (más parámetros específicos)
      - Antes de delegar: verificar que `provider_name` está en `session.providers`. Si no, lanzar `SessionConfigError` con la lista de proveedores disponibles en la sesión
      - Si está: obtener `provider_config = session.providers[provider_name]`, instanciar el proveedor con `ProviderFactory.create(provider_name, provider_config)` y delegar al caso de uso correspondiente
    - _Requisitos: 3.1, 3.5, 4.1, 5.1_

  - [ ]* 10.2 Escribir unit tests para ContextService
    > Verifica que la fachada valida correctamente la sesión y delega al caso de uso correcto.
    - Archivo: `tests/unit/test_context_service.py`
    - Test `SessionConfigError`: llamar cualquier método con un `provider_name` que no está en `session.providers` → verificar que se lanza `SessionConfigError` con mensaje que incluye los proveedores disponibles
    - Test delegación `read_full`: verificar que se llama `ReadFullUseCase.execute()` con los parámetros correctos
    - Test delegación `read_summarize`: verificar que se llama `ReadSummarizeUseCase.execute()` con `max_tokens` correcto
    - Test delegación `read_chunks`: verificar que se llama `ReadChunksUseCase.execute()` con `chunk_indices` correcto
    - _Requisitos: 3.5, 4.1, 5.1_

- [ ] 11. Implementar Interface Layer: Schemas y SessionManager
  > Los schemas Pydantic validan automáticamente el JSON que llega en las requests HTTP. El `SessionManager` guarda en memoria la configuración de cada sesión MCP activa.

  - [ ] 11.1 Implementar schemas Pydantic
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
    - _Requisitos: 1.2, 12.1_

  - [ ] 11.2 Implementar `SessionManager`
    > Guarda en memoria la configuración de cada sesión MCP. Cuando el cliente hace `initialize`, se guarda su config. Cuando hace `tools/call`, se recupera para saber qué proveedores tiene disponibles.
    - Crear `app/session.py`:
      - Clase `SessionManager` con `_sessions: dict[str, SessionConfig] = {}`
      - `store(session_id, config)`: validar antes de guardar:
        - Si `config.providers` está vacío → lanzar `SessionConfigError("La sesión debe tener al menos un proveedor")`
        - Si algún `token` está vacío → lanzar `SessionConfigError("El token del proveedor X no puede estar vacío")`
        - Si es válida: guardar en `_sessions[session_id] = config`
      - `get(session_id)`: retornar `_sessions[session_id]`. Si no existe → lanzar `SessionConfigError("Sesión no encontrada. Llama a initialize primero.")`
      - `delete(session_id)`: eliminar silenciosamente si existe, ignorar si no existe
    - _Requisitos: 1.2, 1.3, 1.4, 1.5_

  - [ ]* 11.3 Escribir property tests para SessionManager
    > Verifica que la validación de sesiones es robusta para cualquier combinación de inputs inválidos.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 1:** Para cualquier `ProviderConfig` con `token` vacío o `base_url` con formato inválido, `store()` siempre lanza `SessionConfigError`.
    - **Propiedad 19:** Para cualquier `SessionConfig` con `providers` vacío, `store()` siempre lanza `SessionConfigError` con un mensaje descriptivo.
    - Comentario: `# Feature: contextforge, Propiedad 1: Validación de campos faltantes en ProviderConfig`
    - _Valida: Requisitos 1.4, 1.5_

- [ ] 12. Implementar Interface Layer: Controllers y Exception Handlers
  > Los controllers son los puntos de entrada HTTP. Reciben la request, la parsean con los schemas Pydantic, delegan al `ContextService` y retornan la respuesta. Los exception handlers capturan errores de dominio y los convierten en respuestas HTTP con el código correcto.

  - [ ] 12.1 Implementar `ApplicationController` base
    > Clase base que todos los controllers heredan. Recibe un `APIRouter` y lo guarda en `self.router` para que los controllers registren sus endpoints en él.
    - Crear `app/controllers/application_controller.py`:
      - Clase `ApplicationController` con constructor `__init__(self, router: APIRouter)` que guarda `self.router = router`
    - _Requisitos: 1.1_

  - [ ] 12.2 Implementar exception handlers globales
    > En lugar de manejar errores en cada endpoint, los handlers globales capturan las excepciones de dominio y retornan la respuesta HTTP correcta automáticamente. `main.py` los registra con `app.add_exception_handler()`.
    - Crear `app/exceptions/exception_handler.py`:
      - Handler async para cada excepción: `session_config_error_handler` → 400, `item_not_found_handler` → 404, `authentication_error_handler` → 401, `validation_error_handler` → 422, `provider_not_registered_handler` → 422, `generic_contextforge_handler` → 422
      - Cada handler retorna `JSONResponse(status_code=X, content={"message": str(exc)})`
      - Exportar `exception_handlers: dict = {SessionConfigError: handler, ...}` para que `main.py` lo itere
    - _Requisitos: 3.5, 3.6, 3.7, 4.7, 5.7_

  - [ ] 12.3 Implementar `HealthController`
    > Endpoint simple para verificar que el servidor está vivo. Útil para Docker healthchecks y monitoreo.
    - Crear `app/controllers/health_controller.py`:
      - Clase `HealthController(ApplicationController)`
      - En `__init__`: registrar `@self.router.get("/health")` que retorna `{"status": "ok"}`
    - _Requisitos: 1.1_

  - [ ] 12.4 Implementar `MCPController`
    > El controller principal. Recibe todas las requests MCP en un único endpoint POST y las despacha según el campo `method` del body JSON.
    - Crear `app/controllers/mcp_controller.py`:
      - Clase `MCPController(ApplicationController)` con constructor que recibe `router`, `context_service` y `session_manager`
      - Registrar `POST /` que despacha según `request.method`:
        - `"initialize"` → `_handle_initialize`: parsear `params.clientInfo.config` como `SessionConfig`, llamar `session_manager.store(session_id, config)`, retornar respuesta MCP con `protocolVersion`, `capabilities: {}` y `serverInfo: {"name": "contextforge", "version": "1.0.0"}`
        - `"tools/list"` → `_handle_tools_list`: retornar lista de las tres herramientas (`read_full`, `read_summarize`, `read_chunks`) con descripciones que guíen al agente a elegir la correcta según su necesidad
        - `"tools/call"` → `_handle_tool_call`: obtener sesión con `session_manager.get(session_id)`, despachar a `context_service.read_full/read_summarize/read_chunks` según `params.name`, serializar y retornar la respuesta
        - Cualquier otro método → retornar `JSONResponse({"message": "Método no soportado"}, status_code=400)`
      - Registrar `GET /` que retorna `{"message": "SSE endpoint activo"}` (stub para compatibilidad con spec MCP 2025-03-26)
    - _Requisitos: 1.1, 1.2, 1.3, 1.6, 3.1, 4.1, 5.1, 12.1, 12.3, 12.4_

  - [ ]* 12.5 Escribir property tests para validaciones del MCPController
    > Verifica que el controller rechaza correctamente inputs inválidos y que las respuestas contienen solo el contexto solicitado.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 2:** Para cualquier `base_url` con formato inválido (sin `http://` o `https://`, con espacios, etc.), el sistema retorna error antes de intentar conectarse al proveedor.
    - **Propiedad 17:** La respuesta de `tools/call` contiene exactamente el contenido solicitado: `read_full` retorna el texto completo, `read_summarize` retorna solo el resumen, `read_chunks` retorna solo los chunks pedidos.
    - Comentario: `# Feature: contextforge, Propiedad 2: Rechazo de URL con formato inválido`
    - _Valida: Requisitos 1.5, 12.3_


- [ ] 13. Implementar `settings.py` y `main.py`
  > El punto de entrada de la aplicación. `settings.py` carga y valida las variables de entorno al arrancar. `main.py` crea la app FastAPI, conecta todos los componentes y registra las rutas.

  - [ ] 13.1 Implementar `settings.py`
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
    - _Requisitos: 2.1, 2.3, 2.4, 2.5, 11.2, 11.6_

  - [ ]* 13.2 Escribir property test para settings
    > Verifica que el servidor falla al arrancar si faltan variables de entorno requeridas.
    - Archivo: `tests/property/test_properties_validation.py`
    - **Propiedad 15:** Para cualquier combinación de variables de entorno donde `LLM_API_KEY` está ausente o vacía, la inicialización de `Settings` lanza un error (o llama `sys.exit(1)`). Con `LLM_API_KEY` presente, siempre inicializa correctamente.
    - Usar `unittest.mock.patch.dict(os.environ, {...})` para simular variables de entorno
    - Comentario: `# Feature: contextforge, Propiedad 15: Fallo al iniciar con variables de entorno requeridas faltantes`
    - _Valida: Requisito 2.4_

  - [ ] 13.3 Implementar `main.py` y `config/routes.py`
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
    - _Requisitos: 1.1, 2.2, 10.3, 11.3_

- [ ] 14. Implementar property tests de caché
  > Tests que verifican el comportamiento del sistema de caché de extremo a extremo: que los datos se guardan y recuperan correctamente, y que la caché se invalida cuando el contenido cambia.

  - [ ]* 14.1 Escribir property tests para comportamiento de caché
    > Verifica las propiedades fundamentales del sistema de caché usando mocks de ChromaDB.
    - Archivo: `tests/property/test_properties_cache.py`
    - **Propiedad 3:** Para cualquier `CacheEntry` almacenada con `store()`, una llamada inmediata a `lookup()` con los mismos parámetros siempre retorna la misma entrada con `from_cache=True` (round-trip).
    - **Propiedad 11:** Si el `content_hash` de un ítem cambia (el contenido fue modificado en el proveedor), `lookup()` con el nuevo hash retorna `None` (cache miss), forzando la regeneración del contenido.
    - Comentario: `# Feature: contextforge, Propiedad 3: Round-trip de caché por herramienta`
    - _Valida: Requisitos 3.4, 4.6, 5.6, 6.3, 6.5_

- [ ] 15. Checkpoint final — Integración completa
  > Verificación final de que todo el sistema funciona de extremo a extremo: tests, servidor y Docker.
  - Ejecutar todos los tests: `pytest tests/ -v` y verificar que todos pasan
  - Verificar que el servidor arranca correctamente: `uvicorn main:app --port 8999`
  - Verificar que `GET /health` retorna `{"status": "ok"}`
  - Verificar que `docker-compose up` levanta ambos servicios (`contextforge` y `chromadb`) sin errores
  - Preguntar al usuario si hay dudas o ajustes antes de cerrar el spec
