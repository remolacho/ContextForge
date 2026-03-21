# Workflow: Ejecución

## Regla Principal

**Para cada paso del plan:**
1. Mostrar descripción
2. Esperar "next"
3. Ejecutar
4. make check
5. Actualizar sesión

---

## Validación

Verificar PLAN completado en sesión.

Si no completado → Error: "Completa PLAN primero"

---

## Leer sesión activa

```bash
ls -la .context/session_*.md | tail -1
```

Mostrar resumen de progreso.

---

## Ejecución de Pasos

### Para cada paso del plan:

#### 1. MOSTRAR descripción

```
================================================================
PASO N DE M: [nombre del paso]
================================================================

Descripción: ...
Archivos: ...

Skill aplicable: ...
================================================================
```

#### 2. ESPERAR "next"

**Esperar "next" o "abort".**

#### 3. EJECUTAR

1. Ejecutar código
2. make check
3. Reportar resultado

#### 4. Si FALLA

```
ERROR: make check FALLÓ

LINT: ...
TYPECHECK: ...
TESTS: ...

Esperar "retry" o "abort".
```

#### 5. Si PASA

Marcar paso completado en sesión.

---

## Verificación Final

Después de completar todos los pasos:

```bash
make lint
make typecheck
make test
```

Mostrar resultados.

---

## Continuar

Esperar "next" para continuar a FINALIZE.

→ Leer `finalize_workflow.md`

---

## Comandos

| Comando | Qué |
|---------|-----|
| `make check` | lint + typecheck + test |
| `next` | Siguiente paso |
| `abort` | Detener |
| `retry` | Reintentar make check |
