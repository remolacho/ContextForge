# Wait Abort

## Description
Wait for user to decide between retry or abort.

## Commands
- `retry` - Retry failed operation
- `abort` - Stop workflow

## Behavior
Used after `make check` fails.

## Prompt
```
ERROR: Operation failed.

Esperar "retry" o "abort".
```

## Transitions

| Input | Next Step |
|-------|-----------|
| `retry` | Retry operation |
| `abort` | Stop workflow |

## Next Step
Based on user input
