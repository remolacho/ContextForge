# Arquitectura de referencia: API FastAPI

Documento para que otro sistema arme una estructura básica con FastAPI: rutas, manejo de errores y serialización con Pydantic. Incluye un ejemplo de endpoint de punta a punta.

---

## 1. Configuración de rutas

### 1.1 Aplicación principal

**Ubicación:** `main.py` en la raíz.

| Elemento | Especificación |
|----------|----------------|
| Framework | FastAPI |
| Parámetros | `title`, `description`, `version` |
| Documentación | `docs_url="/docs"`, `redoc_url="/redoc"`, `openapi_url="/openapi.json"` |

**Orden en `main.py`:**

1. Crear instancia de FastAPI.
2. Registrar exception handlers (sección 2).
3. Añadir middlewares (CORS, etc.).
4. Registrar rutas (p. ej. `Routes(app).register()`).

### 1.2 Router principal

**Ubicación:** `config/routes.py` (o equivalente).

- Un único `APIRouter(responses={404: {"description": "Not found"}})` sin prefix, o con el prefix que se desee.
- Por cada controller: `app.include_router(Controller(router).router)` pasando el mismo `router`. Cada controller registra sus rutas sobre ese router en su `__init__`.

### 1.3 Controllers

**Ubicación:** `app/controllers/`, por recurso.

- **Base:** recibe un `APIRouter` y guarda en `self.router`.
- **Concreto:** hereda la base; en `__init__` asigna `self.router.tags = ["NombreTag"]` y define los endpoints con `@self.router.get(...)` / `@self.router.post(...)` etc., con `path`, `response_model`, `status_code` y `responses`.

---

## 2. Manejo de excepciones

### 2.1 Registro

- **Módulo:** `app/exceptions/exception_handler.py`.
- **En `main.py`:** un diccionario mapea tipo de excepción → handler; se hace `app.add_exception_handler(exc, handler)` por cada par.

### 2.2 Excepciones y códigos HTTP

| Excepción | Código HTTP |
|-----------|-------------|
| `ResourceNotFoundException(message, ...)` | 404 |
| `ForbiddenException(message)` | 403 |
| `NoResultFound` (SQLAlchemy) | 404 |
| `Exception` (genérico) | 422 |

### 2.3 Formato de respuesta de error

Sin estructura compleja: **no** usar `success` ni `data`. Respuesta plana, por ejemplo solo el mensaje o pocos campos:

```json
{
  "message": "Recurso no encontrado"
}
```

O con contexto mínimo:

```json
{
  "message": "Recurso no encontrado",
  "resource_id": "123"
}
```

Cada handler devuelve `JSONResponse` con `status_code`, `content` (objeto plano como arriba) y los `headers` necesarios (p. ej. CORS).

---

## 3. Serialización con Pydantic

### 3.1 Respuestas exitosas: estructura simple

**No** usar envoltura `success` + `data`. La respuesta es un objeto plano con los campos del recurso.

Ejemplo:

```json
{
  "task_id": "RKM-1225",
  "summary": "Resumen de la tarea...",
  "tokens_used": 480
}
```

### 3.2 Schemas

- **Ubicación:** `app/schemas/`, por recurso.
- Un `BaseModel` por tipo de respuesta, con los campos directos (sin `success` ni `data`).

Para el ejemplo anterior:

```python
from pydantic import BaseModel

class TaskResponse(BaseModel):
    task_id: str
    summary: str
    tokens_used: int
```

En el endpoint se usa `response_model=TaskResponse` y se devuelve `TaskResponse(task_id=..., summary=..., tokens_used=...)`. FastAPI serializa a JSON.

### 3.3 Errores en OpenAPI

- Para documentar errores en Swagger se puede definir un schema plano, p. ej. `ErrorResponse` con solo `message: str`.
- En el decorador del endpoint, en `responses`, se asocia cada código de error a ese modelo y una descripción. El cuerpo real lo generan los exception handlers (objeto plano como en la sección 2.3).

---

## 4. OpenAPI / Swagger

- En el constructor de FastAPI: `docs_url="/docs"`, `redoc_url="/redoc"`, `openapi_url="/openapi.json"`.
- Agrupación por tags: `self.router.tags = ["Tasks"]` (u otro nombre) en cada controller.
- Los modelos que se ven en Swagger son los usados en `response_model` y en `responses`. Opcional: `json_schema_extra` con `example` en el schema para mejorar la doc.

---

## 5. Ejemplo de endpoint completo

Objetivo: un GET que devuelve una "tarea" con estructura simple.

### 5.1 Schema de respuesta

`app/schemas/task.py`:

```python
from pydantic import BaseModel

class TaskResponse(BaseModel):
    task_id: str
    summary: str
    tokens_used: int

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "RKM-1225",
                "summary": "Resumen de la tarea...",
                "tokens_used": 480
            }
        }
```

### 5.2 Schema de error (para documentar en OpenAPI)

`app/schemas/errors.py`:

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    message: str
```

### 5.3 Controller

`app/controllers/tasks/get_controller.py` (o equivalente):

```python
from fastapi import APIRouter, status, Path
from app.controllers.application_controller import ApplicationController
from app.schemas.task import TaskResponse
from app.schemas.errors import ErrorResponse

class GetTaskController(ApplicationController):
    def __init__(self, router: APIRouter):
        super().__init__(router)
        self.router.tags = ["Tasks"]

        @self.router.get(
            "/tasks/{task_id}",
            response_model=TaskResponse,
            status_code=status.HTTP_200_OK,
            responses={
                200: {"description": "Tarea obtenida"},
                404: {"model": ErrorResponse, "description": "No encontrado"},
            },
        )
        async def get_task(task_id: str = Path(..., description="ID de la tarea")):
            # Lógica (servicio, BD, etc.) → result
            result = {"task_id": task_id, "summary": "Resumen...", "tokens_used": 480}
            return TaskResponse(**result)
```

### 5.4 Registro del router

En `config/routes.py`:

```python
self.app.include_router(GetTaskController(self.router).router)
```

### 5.5 Respuesta del endpoint

**GET /tasks/RKM-1225** → 200:

```json
{
  "task_id": "RKM-1225",
  "summary": "Resumen de la tarea...",
  "tokens_used": 480
}
```

**Error (p. ej. 404)** → cuerpo plano:

```json
{
  "message": "Recurso no encontrado"
}
```

---

## Resumen para otro sistema

1. **FastAPI:** instancia en `main.py` con `docs_url="/docs"`, `redoc_url="/redoc"`, `openapi_url="/openapi.json"`.
2. **Rutas:** un `APIRouter()` (sin prefix o el que se necesite); controllers que reciben ese router y registran endpoints con `response_model`, `status_code` y `responses`.
3. **Errores:** handlers que devuelven `JSONResponse` con cuerpo plano (p. ej. solo `message`), sin `success` ni `data`.
4. **Serialización:** schemas Pydantic con campos directos (objeto plano); sin envoltura `success`/`data` en respuestas exitosas.
5. **Ejemplo:** un GET como `/tasks/{task_id}` que devuelve `TaskResponse(task_id, summary, tokens_used)` y documenta 404 con `ErrorResponse(message)`.

Con esto otro sistema puede armar una estructura básica y un endpoint de ejemplo siguiendo el mismo patrón.
