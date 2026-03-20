---
inclusion: manual
---

# Skill: Providers

Adaptadores para fuentes de datos externas.

## Archivos

```
src/infrastructure/providers/
├── factory.py           # ProviderFactory
├── task/
│   └── youtrack.py      # YouTrackProvider
└── git/
    └── github.py        # stub
```

## ProviderFactory

Instancia el provider según `config.code`.

```python
class ProviderFactory:
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def create(self) -> ProviderInterface:
        code = self.config.code
        if code == "youtrack":
            return YouTrackProvider(self.config)
        raise ProviderNotRegisteredError(...)
```

## YouTrackProvider

```python
class YouTrackProvider(ProviderInterface):
    def __init__(self, config: ProviderConfig):
        self._config = config

    def get_item(self, item_id: str, config: ProviderConfig) -> ContextItem:
        url = f"{config.base_url}/api/issues/{item_id}"
        headers = {"Authorization": f"Bearer {config.token}"}
        # GET request, map response to ContextItem
        return ContextItemBuilder()...
```

## Convenciones

- Cada provider transforma su JSON específico a campos genéricos
- Usa `ContextItemBuilder` para construir el resultado
- Maneja errores: 401/403 → `AuthenticationError`, 404 → `ItemNotFoundError`, 5xx → `ProviderServerError`

## Agregar Nuevo Provider

1. Crear archivo en `src/infrastructure/providers/<tipo>/`
2. Implementar `ProviderInterface`
3. Agregar `if` en `ProviderFactory.create()`
4. Actualizar mensaje de error con nuevos disponibles

## Referencia

Ver `.kiro/specs/contextforge/design.md` sección Providers.
