# Session Create

## Description
Create a new session file with timestamp.

## Command
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_FILE=".context/session_${TIMESTAMP}.md"
```

## Template
Use `session-template.md` from `.agents/templates/`

## Fields to Fill
- Fecha: {YYYY-MM-DD}
- Hora: {HH:MM:SS}
- Rama: {branch-name}

## Next Step
Return to invoking workflow
