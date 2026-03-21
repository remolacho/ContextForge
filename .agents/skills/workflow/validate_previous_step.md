# Validate Previous Step

## Description
Validate that previous workflow step was completed before proceeding.

## CRITICAL RULE
```
Al iniciar PASO N → Verificar PASO N-1 completado
Si no completado → Error: "Completa paso {N-1} primero"
```

---

## Step Dependencies

| Al iniciar | Validar | Si falla |
|------------|---------|----------|
| PLAN (4) | INIT (3) completado | Error: "Completa INIT primero" |
| EXECUTE (5) | PLAN (4) + Rama validada | Error: "Completa PLAN y valida rama primero" |
| FINALIZE (6) | EXECUTE (5) completado + make check | Error: "Completa EXECUTE y pasa make check primero" |

---

## Validation Commands

### 1. Check Session File
```bash
ls -la .context/session_*.md 2>/dev/null | tail -1
```

### 2. Read Session Content
```bash
cat .context/session_*.md
```

Expected format:
```markdown
# Sesión de Trabajo

| Paso | Estado | Descripción |
|------|--------|-------------|
| 1. start | ✅ | Completado |
| 2. INIT | ✅ | Mostrar rol, reglas |
| 3. TASK_SOURCE | ✅ | Fuente: YouTrack, Rama: feature |
| 4. PLAN | ✅ | Plan generado, Rama: feature/MCF-XXX-creada |
| 5. EXECUTE | ⏳ | En progreso |
| 6. FINALIZE | ⏸️ | Pendiente |
```

---

## Validation Matrix

### INIT (Paso 2)
Antes de INIT → Verificar que session fue creada por start.

### TASK_SOURCE (Paso 3)
Antes de TASK_SOURCE → Verificar INIT completado.

Validar:
- YouTrack issue ID (MCF-XXX) obtenido
- Rama tipo seleccionada (feature/hotfix)

### PLAN (Paso 4)
Antes de PLAN → Verificar TASK_SOURCE completado.

Validar:
- Plan generado
- Rama nombre definido
- YouTrack actualizado

### EXECUTE (Paso 5)
Antes de EXECUTE → Verificar PLAN completado.

Validar:
1. Rama creada: `git branch --show-current` returns non-empty
2. Rama nombre válido: matches `feature/MCF-XXX-...` or `hotfix/MCF-XXX-...`
3. Rama base correcta: checked out from `development` or `main`

**NO CONTINUAR si la rama no está validada.**

### FINALIZE (Paso 6)
Antes de FINALIZE → Verificar EXECUTE completado.

Validar:
1. Todos los pasos de ejecución completados
2. `make check` pasa (lint + typecheck + test)

---

## Error Messages

### INIT sin start
```
❌ ERROR: No hay sesión activa.

Ejecuta 'start' primero para crear una sesión.
```

### TASK_SOURCE sin INIT
```
❌ ERROR: INIT no completado.

Primero ejecuta los pasos de inicialización.
```

### PLAN sin TASK_SOURCE
```
❌ ERROR: TASK_SOURCE no completado.

Primero:
1. Selecciona fuente de tarea (Archivo o YouTrack)
2. Confirma la tarea
3. Selecciona tipo de rama
```

### EXECUTE sin PLAN
```
❌ ERROR: PLAN no completado.

Primero:
1. Lee plan_workflow.md
2. Genera plan de implementación
3. Crea rama (feature/MCF-XXX-descripcion)
4. Valida que la rama existe
```

### EXECUTE sin Rama Válida
```
❌ ERROR: Rama no creada o no validada.

Pasos requeridos:
1. git checkout -b feature/MCF-XXX-descripcion development
2. Verificar con: git branch --show-current
3. Debe mostrar: feature/MCF-XXX-descripcion

Si escribiste solo "feature" en lugar de "feature/MCF-XXX-descripcion":
  git checkout -b feature/MCF-XXX-descripcion development

Luego intenta 'next' nuevamente.
```

### FINALIZE sin EXECUTE
```
❌ ERROR: EXECUTE no completado.

Primero completa todos los pasos de ejecución:
1. make check debe pasar
2. Responder 'next' al finalizar
```

---

## Transitions

| Validation | Result | Action |
|------------|--------|--------|
| All checks pass | ✓ | Continue to current step |
| Session missing | ✗ | Show error, abort |
| Previous step not done | ✗ | Show error with required action |
| Branch invalid | ✗ | Show branch creation command |
| make check failed | ✗ | Show check errors |

---

## Next Step
Continue or abort based on validation result
