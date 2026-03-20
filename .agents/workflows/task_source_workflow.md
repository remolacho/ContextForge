# Workflow: Fuente de Tareas

## Flujo: Archivo Local

1. **Solicitar ruta del archivo**
   - Si el usuario proporciona ruta, verificar que existe
   - Si no existe, pedir ruta válida

2. **Leer archivo**
   - Parsear tareas del archivo (formato markdown con listas `- [ ]`)
   - Extraer: título, descripción, subtareas

3. **Listar tareas disponibles**
   - Mostrar cada tarea con índice y título
   - Formato: `[1] Título de tarea`, `[2] Otra tarea`

4. **Solicitar selección**
   - Preguntar: "¿Qué tarea deseas tomar?" (número)
   - Validar selección válida

5. **Crear tarea en YouTrack**
   - **Project:** ContextForge
   - **Sprint:** https://communities.youtrack.cloud/agiles/195-1/current
   - Usar herramienta `youtrack_create_issue`
   - **IMPORTANTE:** Crear UNA sola tarea con TODO el contenido:
     - Mantener descripción completa
     - Subtareas como lista en descripción
     - Preservar estructura y formato original
     - Incluir TODOS los detalles mencionados

6. **Retornar URL de tarea creada**
   - Mostrar link de YouTrack

---

## Flujo: URL YouTrack

1. **Extraer ID de tarea**
   - Parsear URL para obtener issue ID (ej: `MCF-XXX`)

2. **Obtener información de la tarea**
   - Usar herramienta `youtrack_get_issue` con el ID
   - Extraer summary y description

3. **Retornar contenido**
   - Mostrar summary y description

---

## Continuar

Una vez obtenido el contexto de la tarea:
- Solicitar tipo de rama: `hotfix` o `feature`
- hotfix → desde main
- feature → desde development
- Continuar a plan_workflow
