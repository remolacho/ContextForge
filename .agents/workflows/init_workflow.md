# Workflow: Inicialización

## Paso 1: Crear sesión

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_FILE=".context/session_${TIMESTAMP}.md"
```

Crear archivo con session-template.md.

---

## Paso 2: Mostrar rol

```
ROL: Desarrollador Senior Python

Habilidades:
- Clean Architecture y patrones de diseño
- LangChain y LCEL
- Testing con pytest y hypothesis
- Docker y DevOps
- Gestión de proyectos con YouTrack
```

---

## Paso 3: Listar skills

| Skill | Descripción |
|-------|-------------|
| `class_format.md` | Formato de clases (≤15 líneas/método) |
| `controllers.md` | Patrón FastAPI controllers |
| `factories.md` | Patrón Factory |
| `domain_layer.md` | Entidades, interfaces, excepciones |
| `builders.md` | ContextItemBuilder, CacheEntryBuilder |
| `providers.md` | YouTrackProvider, ProviderFactory |
| `cache.md` | ChromaCacheRepository |
| `llm.md` | GeminiLLMEngine, Summarized |

---

## Paso 4: Listar workflows

- init_workflow.md — Inicialización
- task_source_workflow.md — Fuente de tareas
- plan_workflow.md — Planificación
- execute_workflow.md — Ejecución
- finalize_workflow.md — Finalización

---

## Continuar

→ Leer `task_source_workflow.md`
