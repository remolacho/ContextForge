# Workflow: Planificación

## Validación Previa ⚠️

→ Leer `.agents/skills/workflow/validate_previous_step.md`

→ Leer `.agents/skills/session/read.md`

Antes de iniciar PLAN, verificar TASK_SOURCE completado:

| Check | Validar |
|-------|---------|
| Sesión existe | .context/session_*.md |
| TASK_SOURCE | YouTrack ID (MCF-XXX) obtenido |
| Tipo_rama | feature o hotfix seleccionado |

**Si no completado:**
```
❌ ERROR: TASK_SOURCE no completado.

Primero completa:
1. Selecciona fuente de tarea
2. Confirma la tarea
3. Selecciona tipo de rama
```

→ Leer `.agents/skills/session/update.md`

Actualizar sesión:
```markdown
| 4. Tipo_rama | ✅ | {feature/hotfix} |
```

---

## Pasos

### Paso 1: Extraer contexto

Leer:
1. `tasks.md` — Tarea seleccionada
2. `.agents/docs/init_proyect/requirements.md` — Criterios de aceptación

---

### Paso 2: Identificar reglas aplicables

→ Leer `.agents/skills/workflow/identify_rules.md`

| Regla | Propósito |
|-------|------------------|
| `.agents/rules/*.md` | Reglas específicas de implementación |

---

### Paso 3: Crear plan

→ Leer `.agents/skills/workflow/generate_plan.md`

Dividir en pasos:
- Archivo(s) a crear
- Archivo(s) a modificar
- Test(s) a escribir

---

### Paso 4: Mostrar plan

```
PLAN DE IMPLEMENTACIÓN
============================================================
Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion / hotfix/MCF-XXX-descripcion

PASOS:
[1] Crear archivo X
[2] Implementar funcionalidad Y
[3] Escribir tests
============================================================
```

→ Leer `.agents/templates/plan_template.md`

---

### Paso 5: Crear rama

→ Leer `.agents/skills/git/create_branch.md`

```bash
# feature
git checkout -b feature/MCF-XXX-descripcion development

# hotfix
git checkout -b hotfix/MCF-XXX-descripcion main
```

---

### Paso 5b: VALIDAR Rama Creada ⚠️ CRÍTICO

→ Leer `.agents/skills/git/validate_branch.md`

Ejecutar validación antes de continuar:

1. Verificar que la rama existe
2. Verificar formato correcto (feature/MCF-XXX-... o hotfix/MCF-XXX-...)
3. Verificar base branch correcta
4. Verificar working directory limpio

**NO CONTINUAR a YouTrack hasta que la rama esté validada.**

---

### Paso 6: Actualizar YouTrack

→ Leer `.agents/skills/youtrack/update_issue.md`

Usar `youtrack_update_issue`:
- Cambiar estado a "En curso"

---

### Paso 7: Validar Rama ⚠️ CRÍTICO

→ Leer `.agents/skills/git/validate_branch.md`

Ejecutar verificación completa:

```bash
# 1. Verificar rama existe
git branch --show-current

# 2. Verificar formato
# Debe ser: feature/MCF-XXX-descripcion o hotfix/MCF-XXX-descripcion

# 3. Verificar working directory
git status --porcelain
```

**Si validación falla:**
```
❌ ERROR: Rama no válida.

La rama debe existir y tener formato correcto antes de continuar.

Si escribiste mal el nombre (ej: solo "feature"):
  git branch -m feature feature/MCF-XXX-descripcion

Si no creaste la rama:
  git checkout -b feature/MCF-XXX-descripcion development

Verifica con: git branch --show-current
```

**Si validación pasa:**
```
✅ Rama validada: feature/MCF-XXX-descripcion
✅ Ready para ejecución.
```

→ Leer `.agents/skills/session/update.md`

Actualizar sesión:
```markdown
| 5. PLAN | ✅ | Plan generado, Rama: feature/MCF-XXX-descripcion validada |
```

---

### Paso 8: Esperar "next"

→ Leer `.agents/skills/workflow/wait_next.md`

```
============================================================
Plan listo. Rama validada.
Responder 'next' para iniciar ejecución.
============================================================
```

---

## Validación Previa a EXECUTE ⚠️ CRÍTICO

Antes de leer execute_workflow.md, verificar:

| Check | Comando | Esperado |
|-------|---------|----------|
| Rama existe | `git branch --show-current` | feature/MCF-XXX-... |
| Rama nombre válido | regex | feature/... o hotfix/... |
| Working dir | `git status --porcelain` | vacío |

**Si no pasa:**
```
❌ ERROR: No puedes continuar a EXECUTE.

La rama debe estar validada antes de ejecutar código.

Vuelve a PLAN y ejecuta:
1. git checkout -b feature/MCF-XXX-descripcion development
2. Verificar con: git branch --show-current
```

---

## Continuar

→ Leer `execute_workflow.md`
