# Plantilla: Commit Message

## Formato

```
{MCF-XXX}: {descripción corta en imperativo}

- {cambio 1}
- {cambio 2}
- {tests agregados/verificados}
```

## Reglas

| Regla | Ejemplo |
|-------|---------|
| Primera línea: `{MCF-XXX}: {verbo imperativo}` | `MCF-123: implementar ContextItemBuilder` |
| Body: lista con cambios | `- Agregar ContextItemBuilder con métodos fluidos` |
| Tests: indicar si se agregaron | `- Agregar property tests para SHA-256` |
| Usar tiempo presente | "implementar" no "implementó" |

## Ejemplo Completo

```
MCF-123: implementar ContextItemBuilder y CacheEntryBuilder

- Agregar ContextItemBuilder con métodos fluidos
- Agregar CacheEntryBuilder con métodos fluidos
- Agregar property tests para hash SHA-256 determinista
- make check pasa (lint, typecheck, tests)
```

## Verificación

Antes de confirmar, verificar:
- [ ] make check pasa
- [ ] ID de YouTrack correcto en primera línea
- [ ] Cambios enumerados claramente
