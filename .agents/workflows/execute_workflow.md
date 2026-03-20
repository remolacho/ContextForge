# Workflow: Ejecución

## Regla Principal

**Esperar "next" del usuario antes de cada paso.**

## Pasos

1. **Para cada paso del plan:**
   - Mostrar descripción del paso
   - Mostrar código/archivos a modificar
   - **Esperar "next" del usuario**
   - Ejecutar SOLO después de confirmación

2. **Después de ejecutar:**
   - Verificar con `make check`
   - Si falla: reportar errores, esperar correcciones
   - Si pasa: continuar al siguiente paso

3. **Verificación final**
   - Ejecutar `make check` completo
   - Mostrar resultados (lint, typecheck, tests)
   - Solo continuar si todo pasa

## Comandos de Verificación

```bash
make lint     # ruff check
make typecheck # mypy
make test     # pytest
make check    # lint + typecheck + test
```

## Confirmación

El usuario responde:
- `"next"` → Continuar al siguiente paso
- `"stop"` → Detener ejecución
- Otra cosa → Interpretar como instrucción

## Manejo de Errores

Si `make check` falla:
1. Mostrar errores específicos
2. Explicar qué necesita arreglarse
3. Esperar corrección o nueva instrucción
