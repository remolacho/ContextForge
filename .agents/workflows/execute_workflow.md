# Workflow: Ejecución

## Validación Previa ⚠️ CRÍTICO

→ Leer `.agents/skills/workflow/validate_previous_step.md`

Antes de iniciar EXECUTE, verificar:

| Check | Validar |
|-------|----------|
| PLAN completado | Plan generado, mostrado, confirmado |
| Rama creada | `git branch --show-current` retorna nombre válido |
| Rama nombre | `feature/MCF-XXX-...` o `hotfix/MCF-XXX-...` |
| Working dir | `git status --porcelain` vacío |

**Si PLAN no completado:**
```
❌ ERROR: PLAN no completado.

Primero completa:
1. Lee plan_workflow.md
2. Genera plan de implementación
3. Muestra plan al usuario
4. Espera 'next'
```

**Si Rama no creada:**
```
❌ ERROR: Rama no creada.

Primero ejecuta en PLAN:
1. git checkout -b feature/MCF-XXX-descripcion development
2. Verificar con: git branch --show-current

No puedes ejecutar código sin una rama válida.
```

---

## Regla Principal

**Para cada paso del plan:**
1. Mostrar descripción
2. Esperar "next"
3. Ejecutar
4. make check
5. Actualizar sesión

---

## Validación

→ Leer `.agents/skills/workflow/validate_previous_step.md`

Si no completado → Error: "Completa PLAN primero"

---

## Validación de Rama ⚠️ CRÍTICO

→ Leer `.agents/skills/git/validate_branch.md`

Antes de iniciar ejecución, verificar:

1. `git branch --show-current` → Rama existe
2. Formato correcto: `feature/MCF-XXX-...` o `hotfix/MCF-XXX-...`
3. Working directory limpio

**Si la rama no está validada:**
```
❌ ERROR: Rama no validada.

Primero ejecuta en PLAN:
  1. Crear rama
  2. Esperar validación de rama
  3. Responder 'next'

No puedes ejecutar código sin una rama válida.
```

---

## Leer sesión activa

→ Leer `.agents/skills/session/read.md`

Mostrar resumen de progreso.

→ Leer `.agents/skills/session/update.md`

Actualizar sesión:
```markdown
| 6. EXECUTE | 🔄 | En progreso |
```

---

## Inicio de Ejecución

→ Leer `.agents/skills/git/validate_branch.md`

Ejecutar validación final:

```bash
# Verificar rama existe y es válida
git branch --show-current

# Verificar working directory
git status --porcelain
```

**Solo iniciar ejecución si rama está validada.**

---

## Ejecución de Pasos

### Para cada paso del plan:

#### 1. MOSTRAR descripción

```
============================================================
PASO N DE M: [nombre del paso]
============================================================

Descripción: ...
Archivos: ...

Reglas aplicables: .agents/rules/*.md
============================================================
```

→ Leer `.agents/skills/workflow/identify_rules.md`

#### 2. ESPERAR "next"

→ Leer `.agents/skills/workflow/wait_next.md`

#### 3. EJECUTAR

1. Ejecutar código
2. → Leer `.agents/skills/checks/make_check.md`
3. Reportar resultado

#### 4. Si FALLA

→ Leer `.agents/skills/workflow/wait_abort.md`

```
ERROR: make check FALLÓ

LINT: ...
TYPECHECK: ...
TESTS: ...

Esperar "retry" o "abort".
```

#### 5. Si PASA

→ Leer `.agents/skills/session/update.md`

Marcar paso completado en sesión.

---

## Verificación Final

Después de completar todos los pasos:

→ Leer `.agents/skills/checks/make_check.md`

Mostrar resultados.

---

## Validación Previa a FINALIZE ⚠️ CRÍTICO

Antes de continuar a FINALIZE, verificar:

| Check | Estado |
|-------|--------|
| Todos los pasos completados | ⏳ |
| make check pasa | ⏳ |

→ Leer `.agents/skills/session/update.md`

Actualizar sesión:
```markdown
| 6. EXECUTE | ✅ | Completado, make check pasado |
```

**Si make check falla:**
```
❌ ERROR: make check FALLÓ.

No puedes continuar a FINALIZE hasta que todos los checks pasen.
Resuelve los errores y ejecuta 'make check' nuevamente.
```

---

## Continuar

→ Leer `.agents/skills/workflow/wait_next.md`

→ Leer `finalize_workflow.md`

---

## Comandos

| Comando | Qué |
|---------|-----|
| make check | lint + typecheck + test |
| next | Siguiente paso |
| abort | Detener |
| retry | Reintentar make check |
