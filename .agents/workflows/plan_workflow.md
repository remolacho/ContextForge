# Workflow: Planificación

## Pasos

### Paso 1: Extraer contexto

Leer:
1. `tasks.md` — Tarea seleccionada
2. `docs/init_proyect/requirements.md` — Criterios de aceptación

---

### Paso 2: Identificar skill

| Skill / Regla | Propósito |
|-------|------------------|
| `interface_layer` | Controllers, Handlers, Schemas, FastAPI |
| `application_layer` | ContextService, Use Cases |
| `domain_layer` | Entities, Interfaces/Ports, Exceptions |
| `infrastructure_layer` | Providers, LLM, Cache, Builders, Factories |
| `patterns_architecture` | Clean Arch, SOLID, Patterns |
| `skills/rules_develop/*.md` | Reglas específicas de implementación |

Leer skill identificado.

---

### Paso 3: Crear plan

Dividir en pasos:
- Archivo(s) a crear
- Archivo(s) a modificar
- Test(s) a escribir

---

### Paso 4: Mostrar plan

```
PLAN DE IMPLEMENTACIÓN
================================================================
Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion / hotfix/MCF-XXX-descripcion

PASOS:
[1] Crear archivo X
[2] Implementar funcionalidad Y
[3] Escribir tests
================================================================
```

---

### Paso 5: Crear rama

```bash
# feature
git checkout -b feature/MCF-XXX-descripcion development

# hotfix
git checkout -b hotfix/MCF-XXX-descripcion main
```

---

### Paso 6: Actualizar YouTrack

Usar `youtrack_update_issue`:
- Cambiar estado a "En curso"

---

### Paso 7: Esperar "next"

```
================================================================
Plan listo. Responder 'next' para iniciar ejecución.
================================================================
```

**Esperar "next" o "stop".**

---

## Continuar

→ Leer `execute_workflow.md`
