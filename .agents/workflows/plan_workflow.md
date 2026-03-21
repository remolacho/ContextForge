# Workflow: Planificación

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

### Paso 6: Actualizar YouTrack

→ Leer `.agents/skills/youtrack/update_issue.md`

Usar `youtrack_update_issue`:
- Cambiar estado a "En curso"

---

### Paso 7: Esperar "next"

→ Leer `.agents/skills/workflow/wait_next.md`

```
============================================================
Plan listo. Responder 'next' para iniciar ejecución.
============================================================
```

---

## Continuar

→ Leer `execute_workflow.md`
