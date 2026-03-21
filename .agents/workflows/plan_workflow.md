# Workflow: Planificación

## Pasos

### Paso 1: Extraer contexto

Leer:
1. `tasks.md` — Tarea seleccionada
2. `design.md` — Arquitectura
3. `requirements.md` — Criterios de aceptación

---

### Paso 2: Identificar skill

Basado en la tarea:

| Skill | Cuando |
|-------|--------|
| `builders.md` | Builders |
| `cache.md` | ChromaCacheRepository |
| `class_format.md` | Cualquiera |
| `controllers.md` | Controllers FastAPI |
| `domain_layer.md` | Entidades, Interfaces, Excepciones |
| `factories.md` | Factory Pattern |
| `llm.md` | LLM/Gemini |
| `providers.md` | Proveedores |

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
