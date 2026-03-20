---
inclusion: manual
---

# Skill: Controllers y Rutas en ContextForge

Patrón estándar para crear controllers FastAPI y registrar rutas en este proyecto.

## Estructura de archivos

```
main.py                          # instancia FastAPI, registra handlers y rutas
config/
  routes.py                      # router principal, incluye todos los controllers
app/
  controllers/
    application_controller.py    # base abstracta
    <recurso>/
      get_controller.py          # un archivo por acción/verbo
  schemas/
    <recurso>.py                 # response models Pydantic
    errors.py                    # ErrorResponse genérico
  exceptions/
    exception_handler.py         # handlers que devuelven JSONResponse
```

## main.py

Orden obligatorio:

```python
from fastapi import FastAPI
from config.routes import Routes
from app.exceptions.exception_handler import register_exception_handlers

app = FastAPI(
    title="ContextForge",
    description="...",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

register_exception_handlers(app)   # 1. exception handlers
# app.add_middleware(...)          # 2. middlewares
Routes(app).register()             # 3. rutas
```

## config/routes.py — Router principal

```python
from fastapi import FastAPI, APIRouter
from app.controllers.tasks.get_controller import GetTaskController

class Routes:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.router = APIRouter(responses={404: {"description": "Not found"}})

    def register(self) -> None:
        self.app.include_router(GetTaskController(self.router).router)
        # agregar más controllers aquí
```

## ApplicationController — base

`app/controllers/application_controller.py`:

```python
from fastapi import APIRouter

class ApplicationController:
    def __init__(self, router: APIRouter) -> None:
        self.router = router
```

## Controller concreto

Un archivo por acción. El controller hereda `ApplicationController`, asigna tags y define los endpoints en `__init__` con decoradores sobre `self.router`.

`app/controllers/tasks/get_controller.py`:

```python
from fastapi import APIRouter, Path, status
from app.controllers.application_controller import ApplicationController
from app.schemas.task import TaskResponse
from app.schemas.errors import ErrorResponse

class GetTaskController(ApplicationController):
    def __init__(self, router: APIRouter) -> None:
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
            # llamar servicio/use case aquí
            result = ...
            return TaskResponse(**result)
```

## Schemas Pydantic

Respuestas planas, sin envoltura `success`/`data`.

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
                "tokens_used": 480,
            }
        }
```

`app/schemas/errors.py`:

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    message: str
```

## Manejo de excepciones

`app/exceptions/exception_handler.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import ItemNotFoundError, AuthenticationError

def register_exception_handlers(app: FastAPI) -> None:
    handlers = {
        ItemNotFoundError: _not_found_handler,
        AuthenticationError: _forbidden_handler,
        Exception: _generic_handler,
    }
    for exc, handler in handlers.items():
        app.add_exception_handler(exc, handler)

async def _not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})

async def _forbidden_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": str(exc)})

async def _generic_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=422, content={"message": str(exc)})
```

Códigos HTTP de referencia:

| Excepción dominio         | HTTP |
|---------------------------|------|
| `ItemNotFoundError`       | 404  |
| `AuthenticationError`     | 403  |
| `ValidationError`         | 422  |
| `Exception` (genérico)    | 422  |

## Convenciones clave

- Un controller por acción/verbo (no agrupar GET + POST en el mismo archivo).
- Los endpoints se definen dentro del `__init__` del controller con `@self.router.<método>`.
- `response_model` siempre declarado; nunca devolver dicts crudos.
- Errores documentados en `responses={}` del decorador usando `ErrorResponse`.
- Los handlers de excepción devuelven `JSONResponse` con cuerpo plano `{"message": "..."}`.
- Las excepciones lanzadas son siempre del dominio (`src/domain/exceptions.py`), nunca HTTPException de FastAPI directamente en la lógica de negocio.
