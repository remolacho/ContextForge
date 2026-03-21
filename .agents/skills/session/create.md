# Session Create

## Description
Create a new session file with timestamp and required fields.

## Command
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_FILE=".context/session_${TIMESTAMP}.md"
```

## Template
Use `session-template.md` from `.agents/templates/`

## Fields to Fill

| Campo | Valor | Requerido |
|-------|-------|-----------|
| Fecha | {YYYY-MM-DD} | Sí |
| Hora | {HH:MM:SS} | Sí |
| Fuente | Archivo / YouTrack | Sí |
| Tarea | MCF-XXX | Sí |
| Rama | feature/MCF-XXX-descripcion | No (llenar en PLAN) |
| Tipo de rama | feature / hotfix | Sí |

## Required Data Before Creation

Antes de crear la sesión en INIT, capturar:
1. Fuente de tarea (Archivo o YouTrack)
2. Tipo de rama (feature o hotfix)

## Validation After Creation

After creating session file:
1. Verify file exists: `ls -la .context/session_*.md`
2. Read file to confirm content
3. Update session at end of each step

## Next Step
Return to invoking workflow
