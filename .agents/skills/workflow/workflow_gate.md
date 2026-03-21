# Workflow Gate

## Description
Enforces sequential workflow validation. Each step must complete before the next.

## Core Rule
```
Al iniciar PASO N → Verificar PASO N-1 completado
Si no completado → Error: "Completa paso {N-1} primero"
```

---

## Gate Checks

### Gate 1: INIT Gate
**Before:** start (buscar sesión)
**Check:** Sesión no existe aún
**Pass:** Crear sesión nueva
**Fail:** N/A (primera vez)

### Gate 2: TASK_SOURCE Gate
**Before:** TASK_SOURCE
**Check:** INIT completado
**Pass:** Continue
**Fail:** "Completa INIT primero"

### Gate 3: PLAN Gate
**Before:** PLAN
**Check:** TASK_SOURCE completado con:
- YouTrack ID (MCF-XXX)
- Tipo de rama (feature/hotfix)
**Pass:** Continue
**Fail:** "Completa TASK_SOURCE primero"

### Gate 4: EXECUTE Gate ⚠️ CRITICAL
**Before:** EXECUTE
**Check:** 
1. PLAN completado
2. Rama creada y validada
3. `git branch --show-current` returns valid name
**Pass:** Continue to execute
**Fail:** "Completa PLAN y valida rama primero"

**If branch issue:**
```
❌ Rama no válida.

Fix:
  git checkout -b feature/MCF-XXX-descripcion development
  
Verify:
  git branch --show-current
```

### Gate 5: FINALIZE Gate ⚠️ CRITICAL
**Before:** FINALIZE
**Check:**
1. EXECUTE completado
2. `make check` passes
**Pass:** Continue to finalize
**Fail:** "Completa EXECUTE y pasa make check"

---

## Validation Commands

### Check Session
```bash
cat .context/session_*.md
```

### Check Branch
```bash
git branch --show-current
```

### Check Working Dir
```bash
git status --porcelain
```

### Run Make Check
```bash
make check
```

---

## Error Message Template

```
============================================================
❌ VALIDACIÓN FALLIDA
============================================================

Paso actual: {N}
Paso requerido: {N-1}

No puedes continuar hasta que {N-1} esté completo.

Revisar sesión: cat .context/session_*.md

============================================================
```

---

## Success Message Template

```
============================================================
✅ VALIDACIÓN PASADA
============================================================

Paso actual: {N}
Anterior: {N-1} ✅

Continuando...
============================================================
```

---

## Next Step
Return to invoking workflow or abort
