# Workflow: Planificación

## Pasos

1. **Extraer contexto**
   - Leer: tasks.md (tarea seleccionada)
   - Leer: design.md (arquitectura)
   - Leer: requirements.md (criterios)
   - Identificar skill aplicable según la tarea

2. **Mostrar skill relevante**
   - Cargar skill correspondiente de `skills/`
   - Mostrar estructura y convenciones

3. **Crear plan de implementación**
   - Basado en descripción de tarea
   - Identificar archivos a crear/modificar
   - Dividir en pasos ejecutables

4. **Mostrar plan completo**
   - Usar `.agents/templates/plan_template.md`
   - Incluir: ID de tarea, rama, pasos numerados
   - Archivos a crear/modificar

5. **Esperar confirmación**
   - Mostrar "Responde 'next' para iniciar la ejecución"
   - NO ejecutar hasta recibir confirmación

6. **Actualizar estado YouTrack a "En Curso"**
   - Al recibir "next" y antes de iniciar la ejecución
   - Usar herramienta `youtrack_update_issue`
   - Cambiar estado a "En curso" (In Progress)

## Formato del Plan

| Campo | Descripción |
|-------|-------------|
| ID Tarea | MCF-XXX de YouTrack |
| Rama | feature/MCF-XXX-descripcion |
| Pasos | Lista numerada con archivos |
| Skill | Skill aplicable |

## Validaciones

- Rama debe existir en remote
- Tarea en YouTrack debe estar creada
- make check disponible
