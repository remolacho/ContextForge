from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    AuthenticationError,
    ContextForgeError,
    ItemNotFoundError,
    ProviderNotRegisteredError,
    SessionConfigError,
    ValidationError,
)


async def session_config_error_handler(request: Request, exc: SessionConfigError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def item_not_found_handler(request: Request, exc: ItemNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


async def authentication_error_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"message": str(exc)})


async def provider_not_registered_handler(
    request: Request, exc: ProviderNotRegisteredError
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"message": str(exc)})


async def generic_contextforge_handler(request: Request, exc: ContextForgeError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"message": str(exc)})


exception_handlers: dict = {
    SessionConfigError: session_config_error_handler,
    ItemNotFoundError: item_not_found_handler,
    AuthenticationError: authentication_error_handler,
    ValidationError: validation_error_handler,
    ProviderNotRegisteredError: provider_not_registered_handler,
    ContextForgeError: generic_contextforge_handler,
}
