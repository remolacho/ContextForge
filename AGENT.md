# ContextForge Developer Agent

## Rol
[Referencia a .agents/prompts/role.md]

## Skills
Usar los skills del proyecto según la tarea:
- skills/class_format.md: Formato de clases
- skills/controllers.md: Patrones de controllers
- skills/factories.md: Patrón Factory

## Workflows

### Planificación
[Referencia a .agents/workflows/plan_workflow.md]

### Ejecución
[Referencia a .agents/workflows/execute_workflow.md]

### Finalización
[Referencia a .agents/workflows/finalize_workflow.md]

## YouTrack

**Sprint:** https://communities.youtrack.cloud/agiles/195-1/current

Todas las tareas se crean y actualizan en este sprint.

## Reglas

| Regla | Descripción |
|-------|-------------|
| Un solo commit por PR | Squash antes de push |
| Espera "next" | Cada paso requiere confirmación |
| make check | Debe pasar antes de finalizar |
| ID en commits | Incluir ID de YouTrack |
| YouTrack | Todas las tareas en el sprint indicado |

## Flujo Principal

1. Usuario indica que quiere planificar/implementar algo
2. Identificar tipo de rama:
   - hotfix → desde main
   - feature → desde development
3. Ejecutar workflows en secuencia:
   - plan_workflow → execute_workflow → finalize_workflow
