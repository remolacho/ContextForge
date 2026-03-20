# Workflow: Ejecución

## Regla Principal

**ESPERAR "next" del usuario ANTES de cada paso. NO ejecutar sin confirmación.**
**El archivo de sesión se actualiza en `.context/session_*.md` después de cada paso completado.**

---

## Validación de Sesión

### Verificar TASK_SOURCE completado

Antes de iniciar, verificar en sesión:

```markdown
| Flujo | Estado |
|-------|--------|
| TASK_SOURCE | ✅ |
| PLAN | 🔄 |
```

Si TASK_SOURCE no está completado → Error: "Completa TASK_SOURCE primero"

---

## Preparación Inicial

### Leer sesión activa

```bash
ls -la .context/session_*.md | tail -1
```

Mostrar resumen de progreso:
```
================================================================
SESIÓN ACTIVA
================================================================
Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion

Progreso:
- INIT: ✅
- TASK_SOURCE: ✅
- PLAN: ✅
- EXECUTE: 🔄 En progreso
================================================================
```

---

## Actualizar sesión al iniciar EXECUTE

```markdown
## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | ✅ | Completado |
| PLAN | ✅ | Completado |
| EXECUTE | 🔄 | En progreso |
| FINALIZE | ⏳ | No iniciado |
```

---

## Estructura del Workflow

```
┌─────────────────────────────────────┐
│        EJECUCIÓN DE PASOS           │
│                                     │
│  Para cada paso del plan:           │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ MOSTRAR paso                  │  │
│  │   ↓                           │  │
│  │ Leer sesión actual             │  │
│  │ Mostrar progreso de pasos     │  │
│  │   ↓                           │  │
│  │ ESPERAR "next" ←──────────────│──│── Usuario confirma
│  │   ↓                           │  │
│  │ EJECUTAR código               │  │
│  │   ↓                           │  │
│  │ make check                    │  │
│  │   ↓                           │  │
│  │ ¿Pasa?                        │  │
│  │   ├── SÍ → marcar paso ✅     │  │
│  │   │     → siguiente paso      │  │
│  │   └── NO → esperar solución   │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

---

## Ejecución de Cada Paso

### Para cada paso del plan:

---

#### 1. MOSTRAR descripción del paso

```
================================================================
PASO 3 DE 5: Implementar ContextItemBuilder
================================================================

Descripción: Crear builder para construir ContextItem
Archivos: src/infrastructure/builders/context_item.py

Skill aplicable: builders.md

Sesión actual:
- [ ] Paso 1
- [ ] Paso 2 ← actual
- [ ] Paso 3
================================================================
```

---

#### 2. MOSTRAR archivos a modificar

```
Archivos a crear/modificar:
- src/infrastructure/builders/context_item.py (CREAR)
```

---

#### 3. Verificar progreso en sesión

Mostrar qué pasos están completados vs pendientes:
```
Progreso:
- [x] Paso 1
- [ ] Paso 2 ← actual
- [ ] Paso 3
```

---

#### 4. ESPERAR confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR "next".

```
¿Ejecutamos este paso? Responde 'next' para continuar.
```

| Respuesta | Acción |
|-----------|--------|
| "next" | Continuar a paso 5 |
| "stop" | Detener ejecución |
| "skip" | Saltar este paso (requiere confirmación) |
| "abort" | Abortar ejecución |
| Otra cosa | Mostrar opciones válidas |

---

#### 5. EJECUTAR el paso

Después de recibir "next":

1. Ejecutar el código/crear archivos
2. Ejecutar `make check` para verificar
3. Reportar resultado

---

#### 6. Actualizar sesión después de ejecutar

```markdown
### EXECUTE
- [x] Paso 1: ...
- [x] Paso 2: Implementar ContextItemBuilder
- [ ] Paso 3: ...
```

---

#### 7. Verificar con `make check`

```bash
make check
```

| Resultado | Acción |
|-----------|--------|
| PASA | Marcar paso completado → Continuar al siguiente paso |
| FALLA | Ir a "Manejo de Errores" |

---

## Manejo de Errores

Si `make check` FALLA:

### Mostrar errores

```
================================================================
ERROR: make check FALLÓ
================================================================

LINT:
  src/infrastructure/builders/context_item.py:10: E501 line too long

TYPECHECK:
  src/infrastructure/builders/context_item.py:15: error: Missing return type

TESTS:
  tests/unit/test_context_item_builder.py::test_build FAILED
```

---

### Solicitar corrección

**ACCIÓN REQUERIDA:** ESPERAR input del usuario.

```
Corrige los errores y responde:
- 'retry' → Ejecutar make check de nuevo
- 'skip' → Saltar verificación (NO recomendado)
- 'abort' → Abortar ejecución
```

---

### Después de corrección

- Si "retry": ejecutar `make check` de nuevo
- Si pasa: marcar paso completado → continuar al siguiente paso
- Si falla: volver a mostrar errores

---

## Verificación Final

Después de completar TODOS los pasos del plan:

### Ejecutar `make check` completo

```bash
make lint
make typecheck
make test
```

### Mostrar resultados

```
================================================================
VERIFICACIÓN FINAL
================================================================
LINT:       ✓ PASÓ
TYPECHECK:  ✓ PASÓ
TESTS:      ✓ PASÓ (31 passed)
================================================================
```

---

## Actualizar sesión al completar EXECUTE

```markdown
## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | ✅ | Completado |
| PLAN | ✅ | Completado |
| EXECUTE | ✅ | Completado |
| FINALIZE | 🔄 | Esperando iniciar |
```

---

## Continuar a Finalización

**ACCIÓN REQUERIDA:** Mostrar opciones.

```
================================================================
¿Continuamos a la fase de finalización?

- 'finalize' → Ir a finalize_workflow.md
- 'fix' → Volver a corregir errores
- 'stop' → Detener (sesión queda pausada)
================================================================
```

| Respuesta | Acción |
|-----------|--------|
| "finalize" | Leer `finalize_workflow.md` e iniciar |
| "fix" | Volver a errores para corregir |
| "stop" | Detener, sesión queda pausada |

**NOTA:** "next" NO está permitido para continuar. Solo "finalize" permite pasar a la siguiente fase.

---

## Comandos de Verificación

| Comando | Qué verifica |
|---------|-------------|
| `make lint` | ruff check (E, F, I) |
| `make typecheck` | mypy src/ app/ |
| `make test` | pytest tests/ -v |
| `make check` | lint + typecheck + test |
| `make format` | ruff format . |

---

## Estados de Espera

| Momento | ¿Espera? | Qué espera |
|---------|----------|------------|
| Antes de cada paso | **SÍ** | "next" |
| Después de ejecutar | No | make check automático |
| Si make check falla | **SÍ** | "retry" / "skip" / "abort" |
| Verificación final | **SÍ** | "finalize" / "fix" / "stop" |

---

## Continuar

Después de recibir "finalize":
→ Leer `finalize_workflow.md` e iniciar fase de finalización.
→ NO continuar a otra tarea hasta completar finalize.
