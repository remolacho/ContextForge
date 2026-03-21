# YouTrack Create Issue

## Description
Create a new issue in YouTrack.

## Tool
Use `youtrack_create_issue` with the following parameters:

| Parameter | Value |
|-----------|-------|
| project | ContextForge |
| summary | Task title from source file |
| description | Full task description |

## Project Configuration
- Project: ContextForge
- Sprint: https://communities.youtrack.cloud/agiles/195-1/current

## Validation
**OBLIGATORY** when task source is "Archivo local".

## Output
Display created issue URL:
```
Tarea creada en YouTrack:
https://communities.youtrack.cloud/issue/MCF-XXX
```

## Error Handling
If creation fails, show error and abort workflow.

## Next Step
Return to invoking workflow
