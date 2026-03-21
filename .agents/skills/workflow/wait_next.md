# Wait Next

## Description
Wait for user command "next" to continue to next step.

## Command
User types: `next`

## Behavior
- Display prompt to user
- Wait for input
- If "next" → Continue to next step
- If "abort" → Stop workflow

## Prompt
```
============================================================
[STEP DESCRIPTION]
============================================================

Responde 'next' para continuar.
============================================================
```

## Transitions

| Input | Next Step |
|-------|-----------|
| `next` | Continue workflow |
| `abort` | Stop and exit workflow |

## Next Step
Continue to next step in workflow
