# Reglas para Factorías (Pattern: Basic Creator)

Para mantener la consistencia en la creación de objetos por tipo (proveedores, motores, o resolvers), se debe seguir un patrón de factoría básico. Este patrón asegura que la lógica de instanciación esté centralizada en un solo punto, facilitando la mantenibilidad y el reporte de errores por tipos no reconocidos.

## Reglas
1. **Validación Exhaustiva**: La factoría debe lanzar una excepción específica (ej: `ProviderNotRegisteredError`) si el código solicitado no está en el registro.
2. **Encapsulamiento**: La lógica de creación debe estar aislada en el método `create`.
3. **Contratos**: Todos los objetos devueltos deben implementar la interfaz correspondiente definida en el dominio.

## Ejemplo Base (Código Sugerido)

```python
from src.domain.entities import ProviderConfig
from src.domain.exceptions import ProviderNotRegisteredError
from src.domain.interfaces import ProviderInterface

class ProviderFactory:
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def create(self) -> ProviderInterface:
        code = self.config.code
        # Registro explícito de implementaciones
        if code == "youtrack":
            return YouTrackProvider(self.config)
        
        # Error descriptivo por tipo no soportado
        raise ProviderNotRegisteredError(
            f"Proveedor '{code}' no reconocido. Disponibles: youtrack"
        )
```
