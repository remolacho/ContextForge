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

## Paso 3: Listar skills y reglas

| Skill | Capa / Propósito |
|-------|------------------|
| `interface_layer` | Controllers, Handlers, Schemas, FastAPI |
| `application_layer` | ContextService, Use Cases |
| `domain_layer` | Entities, Interfaces/Ports, Exceptions |
| `infrastructure_layer` | Providers, LLM, Cache, Builders, Factories |
| `patterns_architecture` | Clean Arch, SOLID, Patterns |

| Regla de Desarrollo | Descripción |
|-------|-------------|
| `skills/rules_develop/class_format.md` | Formato de clases (≤15 líneas/método) |
| `skills/rules_develop/controllers.md` | Patrón FastAPI controllers |
| `skills/rules_develop/factories.md` | Patrón Factory |
| `skills/rules_develop/domain_layer.md` | Entidades, interfaces, excepciones |
| `skills/rules_develop/builders.md` | ContextItemBuilder, CacheEntryBuilder |
| `skills/rules_develop/providers.md` | YouTrackProvider, ProviderFactory |
| `skills/rules_develop/cache.md` | ChromaCacheRepository |
| `skills/rules_develop/llm.md` | GeminiLLMEngine, Summarized |

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
