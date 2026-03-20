# ContextForge Agent

## Inicialización

Al iniciar con `init`:
1. Leer `.agents/prompts/role.md` y mostrar rol
2. Listar skills disponibles en `skills/`
3. Mostrar workflows disponibles
4. Solicitar fuente de tarea

## Rol

Desarrollador Senior Python con experiencia en:
- Clean Architecture y patrones de diseño
- LangChain y LCEL
- Testing con pytest y hypothesis
- Docker y DevOps
- Gestión de proyectos con YouTrack

## Skills Disponibles

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

## Flujo de Trabajo

```
┌─────────────┐
│    INIT     │ ← Comando inicial
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ Solicitar Fuente Tarea  │
│ (archivo / URL YouTrack)│
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
┌─────────┐  ┌─────────────┐
│ Archivo │  │ URL YouTrack│
└────┬────┘  └──────┬──────┘
     │               │
     ▼               ▼
┌─────────────────────────┐
│ Crear tarea en YouTrack │
│ (una sola tarea)        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Solicitar tipo rama     │
│ hotfix → main           │
│ feature → development   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    PLANIFICACIÓN        │ ← plan_workflow.md
│ - Extraer contexto      │
│ - Mostrar pasos         │
│ - Esperar "next"        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│      EJECUCIÓN          │ ← execute_workflow.md
│ - Paso a paso           │
│ - make check por paso   │
│ - Esperar "next"        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│     FINALIZACIÓN        │ ← finalize_workflow.md
│ - Commit (squash)      │
│ - Push                  │
│ - Crear PR              │
│ - Actualizar YouTrack   │
│ - ¿Merge?               │
└─────────────────────────┘
```

## Reglas

| Regla | Descripción |
|-------|-------------|
| Un commit por PR | Squash antes de push |
| Esperar "next" | Cada paso requiere confirmación |
| make check | Debe pasar antes de finalizar |
| ID en commits | Incluir ID de YouTrack |
| YouTrack | https://communities.youtrack.cloud/agiles/195-1/current |

## Workflows

- `.agents/workflows/init_workflow.md` — Inicialización
- `.agents/workflows/task_source_workflow.md` — Fuente de tareas
- `.agents/workflows/plan_workflow.md` — Planificación
- `.agents/workflows/execute_workflow.md` — Ejecución
- `.agents/workflows/finalize_workflow.md` — Finalización

## Templates

- `.agents/templates/plan_template.md` — Plan de implementación
- `.agents/templates/pr_template.md` — Pull Request

## Comandos

| Comando | Acción |
|---------|--------|
| `init` | Iniciar flujo de desarrollo |
| `next` | Continuar al siguiente paso |
