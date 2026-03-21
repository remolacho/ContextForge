# Git Create Branch

## Description
Create a new branch for the task.

## Commands

### Feature branch
```bash
git checkout -b feature/{MCF-XXX}-description development
```

### Hotfix branch
```bash
git checkout -b hotfix/{MCF-XXX}-description main
```

## Parameters
- `{MCF-XXX}`: YouTrack issue ID
- `description`: Short slug of the task description
- `development` or `main`: Base branch

## Next Step
Return to invoking workflow
