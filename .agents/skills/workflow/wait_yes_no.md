# Wait Yes No

## Description
Wait for user confirmation "si" (yes) or "no".

## Command
User types: `si` or `no`

## Behavior
- Display confirmation prompt
- Wait for input
- If "si" → Continue to next substep
- If "no" → Return to previous step

## Prompt
```
¿Continuar? (si/no)
```

## Transitions

| Input | Next Step |
|-------|-----------|
| `si` | Continue to next substep |
| `no` | Return to previous step |

## Next Step
Based on user input
