# Validate Previous Step

## Description
Validate that previous workflow step was completed.

## Behavior
Check session file for step completion status.

## Validation Rules
```
Al iniciar PASO N → Verificar PASO N-1 completado
Si no completado → Error: "Completa paso {N-1} primero"
```

## Session Check
```bash
ls -la .context/session_*.md | tail -1
```

## Transitions

| Result | Next Step |
|--------|-----------|
| Completed | Continue to current step |
| Not completed | Show error, abort |

## Next Step
Continue or abort based on validation
