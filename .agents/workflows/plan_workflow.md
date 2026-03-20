# Workflow: Planificación

## Pasos

1. **Solicitar fuente de tareas**
   - Preguntar al usuario: "¿De qué archivo quieres tomar las tareas?"
   - Opciones: tasks.md, URL de YouTrack, otro

2. **Mostrar tareas disponibles**
   - Listar todas las tareas con sus IDs y títulos
   - Formato: `[1] Tarea uno`, `[2] Tarea dos`, etc.

3. **Solicitar selección de tarea**
   - Preguntar al usuario: "¿Qué tarea deseas tomar?" (número o letra)
   - Validar que la selección sea válida

4. **Solicitar tipo de rama**
   - hotfix → desde main
   - feature → desde development
   - Descartar si la rama no existe

5. **Crear tarea en YouTrack**
   - **Project:** ContextForge
   - **Sprint:** https://communities.youtrack.cloud/agiles/195-1/current
   - Usar herramienta `youtrack_create_issue`
   - **IMPORTANTE:** Respetar TODO el contenido de la tarea seleccionada en tasks.md
     - Mantener la descripción completa (Goals, Discoveries, etc.)
     - Mantener la estructura y formato original
     - Incluir TODOS los detalles, archivos, directorios mencionados
     - Preservar listas de tareas, referencias y links

6. **Crear rama**
   - Formato: `hotfix/MCF-XXX-descripcion` o `feature/MCF-XXX-descripcion`

7. **Extraer contexto**
   - Leer: tasks.md (tarea seleccionada)
   - Leer: design.md (arquitectura)
   - Leer: requirements.md (criterios)

8. **Mostrar plan completo**
   - Pasos numerados
   - Archivos a crear/modificar
   - Indicar claramente "next" para cada paso

9. **Verificación final y cierre**
   - Al concluir la ejecución del plan, ejecutar `make check` (lint, typecheck, test)
   - Si todo pasa: crear commit, PR y actualizar estado de la tarea en YouTrack
   - Si falla: reportar errores y esperar correcciones
