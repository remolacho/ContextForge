# Workflow: Finalización

## Regla Principal

**7 pasos en orden. Cada uno espera "si" para continuar.**

---

## Validación

→ Leer `.agents/skills/workflow/validate_previous_step.md`

Si no completado → Error: "Completa EXECUTE primero"

---

## PASO 1: Commit

### 1a: Mostrar archivos modificados

→ Leer `.agents/skills/git/show_status.md`

```
PASO 1 DE 7: Commit

Archivos modificados:
- archivo1.py
- archivo2.py
```

### 1b: Esperar "si"

→ Leer `.agents/skills/workflow/wait_yes_no.md`

**Esperar "si" o "abort".**

### 1c: Commit

→ Leer `.agents/skills/git/add_files.md`

→ Leer `.agents/skills/git/commit.md`

---

## PASO 2: Push

### 2a: Mostrar

```
PASO 2 DE 7: Push

Rama: feature/MCF-XXX-descripcion
```

### 2b: Esperar "si"

→ Leer `.agents/skills/workflow/wait_yes_no.md`

### 2c: Push

→ Leer `.agents/skills/git/push.md`

---

## PASO 3: Verificar Commits

### 3a: Mostrar commits

→ Leer `.agents/skills/git/verify_commits.md`

```
PASO 3 DE 7: Verificar Commits

Commits desde origin/development:
- abc1234: Mensaje 1
- def5678: Mensaje 2
```

### 3b: Si más de 1 commit

```
⚠️ IMPORTANTE: PR debe tener 1 commit.
Squash se hará vía GitHub automáticamente.
```

### 3c: Esperar "si"

→ Leer `.agents/skills/workflow/wait_yes_no.md`

---

## PASO 4: Crear PR

### 4a: Generar contenido

Título: `MCF-XXX: título de la tarea`

→ Leer `.agents/templates/pr_template.md`

### 4b: Mostrar preview

```
PASO 4 DE 7: Crear PR

Título: MCF-XXX: título
Base: development
Head: feature/MCF-XXX-descripcion
```

### 4c: Esperar "si"

→ Leer `.agents/skills/workflow/wait_yes_no.md`

### 4d: Crear PR

→ Leer `.agents/skills/git/create_pr.md`

Mostrar URL del PR.

---

## PASO 5: Comentar YouTrack

### 5a: Generar comentario

→ Leer `.agents/templates/pr_template.md`

```
## PR Created

PR: {URL_DEL_PR}

## Resumen de Cambios

- [x] Cambio realizado
- [x] Tests verificados

## Verificación

| Verificación | Estado |
|-------------|--------|
| Lint | ✅ passed |
| Typecheck | ✅ passed |
| Tests | ✅ passed |
```

### 5b: Esperar "si"

→ Leer `.agents/skills/workflow/wait_yes_no.md`

### 5c: Comentar

→ Leer `.agents/skills/youtrack/add_comment.md`

---

## PASO 6: Merge

### 6a: Mostrar

```
PASO 6 DE 7: Merge

¿Hacemos merge del PR?
ADVERTENCIA: Esto mergea a development.
```

### 6b: Esperar "si"

→ Leer `.agents/skills/workflow/wait_yes_no.md`

### 6c: Si "si"

→ Leer `.agents/skills/git/merge_pr.md`

### 6d: Si "no"

Mantener sesión.

---

## PASO 7: Marcar YouTrack como Done

### 7a: Mostrar

```
PASO 7 DE 7: Marcar YouTrack como Done

https://communities.youtrack.cloud/issue/MCF-XXX
```

### 7b: Ejecutar

→ Leer `.agents/skills/youtrack/update_issue.md`

Usar `youtrack_update_issue`:
```json
{
  "issueId": "MCF-XXX",
  "customFields": {"State": "Done"}
}
```

---

## Resumen Final

```
============================================================
✅ WORKFLOW COMPLETADO
============================================================

Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion
PR: https://github.com/.../pull/N

Pasos completados:
[x] Commit
[x] Push
[x] Verificar commits
[x] Crear PR
[x] Comentar YouTrack
[x] Merge
[x] YouTrack Done

Sesión eliminada.
============================================================
```

→ Leer `.agents/skills/session/delete.md`

---

## Estados de Espera

| Paso | Espera |
|------|--------|
| 1. Commit | "si" / "abort" |
| 2. Push | "si" / "abort" |
| 3. Verificar | "si" / "abort" |
| 4. PR | "si" / "abort" |
| 5. YouTrack | "si" / "abort" |
| 6. Merge | "si" / "no" |
| 7. YouTrack Done | automático |
