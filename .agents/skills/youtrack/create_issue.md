# YouTrack Create Issue

## Description
Create ONE issue in YouTrack combining all selected tasks.

## REGLA CRÍTICA: UNA SOLA TAREA

**Sin importar cuántas tareas se seleccionen (1 o 100), se crea UN SOLO issue en YouTrack.**

Las tareas seleccionadas se combinan en:
- **Título:** Primera tarea + " (+N más)" si hay más
- **Descripción:** Lista de todas las tareas en formato markdown

---

## Tool: youtrack_create_issue

Usar `youtrack_create_issue` UNA SOLA VEZ con todos los datos combinados:

```json
{
  "project": "ContextForge",
  "summary": "{título de la primera tarea} (+{N-1} más)",
  "description": "## Tareas del batch\n\n### 1. Título 1\nDescripción 1...\n\n### 2. Título 2\nDescripción 2..."
}
```

---

## Project Configuration
- Project: ContextForge
- Sprint: https://communities.youtrack.cloud/agiles/195-1/current

---

## Validación
**OBLIGATORIO** cuando task source es "Archivo local".

---

## Formatos de Selección (del usuario)

| Formato | Ejemplo | Resultado |
|---------|---------|-----------|
| Número solo | `1` | 1 tarea → 1 YouTrack |
| Números separados | `1,3,5` | 3 tareas → 1 YouTrack con 3 |
| Rango | `1-3` | 3 tareas → 1 YouTrack con 3 |
| "todas" | `todas` | Todas → 1 YouTrack con todas |
| Combinación | `1,3-5,7` | 5 tareas → 1 YouTrack con 5 |

---

## Output Template

```
Creando tarea en YouTrack...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MCF-XXX: Título de la primera tarea (+2 más)
→ https://communities.youtrack.cloud/issue/MCF-XXX ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 1 tarea creada con {N} subtareas combinadas
```

---

## Estructura del Issue Creado

### Título
```
Implementar feature X (+2 más)
```

### Descripción
```markdown
## Tareas del batch

### 1. Título tarea 1
Descripción completa de la tarea 1...

### 2. Título tarea 2
Descripción completa de la tarea 2...

### 3. Título tarea 3
Descripción completa de la tarea 3...
```

---

## Error Handling

Si la creación falla:
```
❌ ERROR: Falló al crear tarea en YouTrack.

Reintentar creación.
Si persiste, abortar workflow.
```

---

## Después de Crear

1. Guardar el ID único creado (MCF-XXX) en sesión
2. Mostrar URL del issue
3. Continuar a selección de tipo de rama

---

## Next Step
Return to invoking workflow
