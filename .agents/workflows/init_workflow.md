---
description: 
---

# Workflow: Inicialización

## Pasos

1. **Mostrar rol**
   - Leer `.agents/prompts/role.md`
   - Mostrar especialidades y principios

2. **Listar skills disponibles**
   - Buscar archivos en `skills/`
   - Mostrar tabla con nombre y descripción breve

3. **Mostrar workflows disponibles**
   - init_workflow
   - task_source_workflow
   - plan_workflow
   - execute_workflow
   - finalize_workflow

4. **Solicitar fuente de tareas**
   - Preguntar: "¿De qué fuente quieres tomar las tareas?"
   - Opciones:
     - Ruta de archivo local (ej: `.kiro/specs/contextforge/tasks.md`)
     - URL de YouTrack (ej: `https://communities.youtrack.cloud/issue/MCF-XXX`)
   - Importante: no muestres rutas el usaurio dara la ruta de la tarea, solo realiza la pregunta

5. **Continuar a task_source_workflow**
   - Si es archivo: listar tareas y solicitar selección
   - Si es URL: leer tarea directamente
