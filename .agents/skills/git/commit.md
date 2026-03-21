# Git Commit

## Description
Create a commit with a structured message.

## Command
```bash
git commit -m "{MCF-XXX}: {description in imperative mood}"
```

## Message Format
```
{MCF-XXX}: {verb in imperative}

- {change 1}
- {change 2}
- {tests added/verified}
```

## Example
```
MCF-123: implement ContextItemBuilder

- Add ContextItemBuilder with fluent methods
- Add property tests for SHA-256
- make check passes
```

## Validation
Before committing, ensure:
- `make check` passes
- YouTrack ID is correct in first line
- Changes are clearly enumerated

## Next Step
Return to invoking workflow
