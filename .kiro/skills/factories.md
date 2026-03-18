---
inclusion: manual
---

# Skill: Factories en ContextForge

Este skill describe el patrón estándar para crear y extender factories en el proyecto ContextForge.

## Patrón general

Las factories en este proyecto siguen un patrón simple y consistente:

- Reciben un objeto de configuración (dataclass del dominio) en `__init__`
- Exponen un único método `create()` que retorna la interfaz del dominio correspondiente
- Si el tipo solicitado no está registrado, lanzan una excepción específica del dominio
- Viven en `src/infrastructure/<subsistema>/factory.py`

## Estructura de archivos

```
src/
  domain/
    entities.py       # dataclasses de config (ej. LLMConfig, ProviderConfig)
    interfaces.py     # ABCs que las implementaciones deben cumplir
    exceptions.py     # excepciones tipadas (ej. LLMEngineNotRegisteredError)
  infrastructure/
    <subsistema>/
      factory.py      # la factory
      <impl>.py       # implementación concreta
```

## Ejemplos reales del proyecto

### LLMFactory — `src/infrastructure/llm/factory.py`

```python
from src.domain.entities import LLMConfig
from src.domain.exceptions import LLMEngineNotRegisteredError
from src.domain.interfaces import LLMEngineInterface
from src.infrastructure.llm.gemini import GeminiLLMEngine


class LLMFactory:
    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def create(self) -> LLMEngineInterface:
        engine_type = self.config.engine_type
        if engine_type == "gemini":
            return GeminiLLMEngine(self.config)
        raise LLMEngineNotRegisteredError(
            f"Motor LLM '{engine_type}' no reconocido. Disponibles: gemini"
        )
```

### ProviderFactory — `src/infrastructure/providers/factory.py`

```python
from src.domain.entities import ProviderConfig
from src.domain.exceptions import ProviderNotRegisteredError
from src.domain.interfaces import ProviderInterface
from src.infrastructure.providers.task.youtrack import YouTrackProvider


class ProviderFactory:
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def create(self) -> ProviderInterface:
        code = self.config.code
        if code == "youtrack":
            return YouTrackProvider(self.config)
        raise ProviderNotRegisteredError(
            f"Proveedor '{code}' no reconocido. Disponibles: youtrack"
        )
```

## Cómo agregar un nuevo tipo a una factory existente

1. Crear la implementación concreta en `src/infrastructure/<subsistema>/<nombre>.py` implementando la interfaz del dominio correspondiente.
2. Importarla en `factory.py`.
3. Agregar un `if` con el identificador string que la config usa (ej. `engine_type`, `code`).
4. Actualizar el mensaje de error con el nuevo nombre disponible.

Ejemplo — agregar soporte para `openai` en `LLMFactory`:

```python
from src.infrastructure.llm.openai import OpenAILLMEngine

# dentro de create():
if engine_type == "openai":
    return OpenAILLMEngine(self.config)
raise LLMEngineNotRegisteredError(
    f"Motor LLM '{engine_type}' no reconocido. Disponibles: gemini, openai"
)
```

## Cómo crear una factory nueva

1. Definir el dataclass de config en `src/domain/entities.py` si no existe.
2. Definir la interfaz ABC en `src/domain/interfaces.py`.
3. Agregar la excepción tipada en `src/domain/exceptions.py` (ej. `class CacheNotRegisteredError(ContextForgeError): ...`).
4. Crear `src/infrastructure/<subsistema>/factory.py` siguiendo el patrón:

```python
from src.domain.entities import <NombreConfig>
from src.domain.exceptions import <NombreNotRegisteredError>
from src.domain.interfaces import <NombreInterface>
from src.infrastructure.<subsistema>.<impl> import <ImplClass>


class <Nombre>Factory:
    def __init__(self, config: <NombreConfig>) -> None:
        self.config = config

    def create(self) -> <NombreInterface>:
        tipo = self.config.<campo_discriminador>
        if tipo == "<valor>":
            return <ImplClass>(self.config)
        raise <NombreNotRegisteredError>(
            f"<Nombre> '{tipo}' no reconocido. Disponibles: <valor>"
        )
```

## Convenciones clave

- El campo discriminador en la config es siempre un `str` simple (ej. `"gemini"`, `"youtrack"`).
- No usar registros dinámicos ni diccionarios de clases — los `if` explícitos son intencionales para mantener legibilidad y trazabilidad estática.
- El mensaje de error siempre lista los valores disponibles para facilitar el debugging.
- Las factories no tienen lógica de negocio, solo instancian y delegan.
