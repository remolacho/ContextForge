# Git Validate Branch

## Description
Validate that a git branch was created correctly.

## Pre-flight Checks

Before continuing from PLAN to EXECUTE:

### 1. Verify Branch Exists
```bash
git branch --show-current
```

Expected: `feature/MCF-XXX-descripcion` or `hotfix/MCF-XXX-descripcion`

### 2. Verify Branch is Based on Correct Base
```bash
git log --oneline -1 HEAD
git merge-base HEAD origin/{base-branch}
```

### 3. Verify No Uncommitted Changes Before Execution
```bash
git status --porcelain
```

If output is empty → Safe to proceed.

---

## Validation Rules

| Check | Command | Expected | If Failed |
|-------|---------|----------|-----------|
| Branch exists | `git branch --show-current` | `feature/MCF-XXX-...` | ERROR: Branch not created |
| Branch name format | pattern match | `feature/...` or `hotfix/...` | ERROR: Invalid branch name |
| Correct base branch | `git merge-base...` | commits from base | ERROR: Wrong base branch |
| Clean working dir | `git status` | empty | ERROR: Uncommitted changes |

---

## Error Messages

### Branch Not Created
```
❌ ERROR: Rama no creada.

Ejecuta:
  git checkout -b feature/MCF-XXX-descripcion development
o
  git checkout -b hotfix/MCF-XXX-descripcion main

Luego intenta 'next' nuevamente.
```

### Wrong Branch Name Format
```
❌ ERROR: Nombre de rama inválido.

Formato esperado:
  - feature/MCF-XXX-descripcion
  - hotfix/MCF-XXX-descripcion

Formato actual: {current_branch}

Renombra con:
  git checkout -b feature/MCF-XXX-descripcion development
```

### Uncommitted Changes
```
❌ ERROR: Tienes cambios sin commit.

Haz commit o descartalos antes de continuar:
  git stash
```

---

## After Validation

If all checks pass:
```
✅ Rama validada correctamente.
✅ lista para ejecutar.
```

Continue to EXECUTE.

---

## Next Step
Return to invoking workflow
