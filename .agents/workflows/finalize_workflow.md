# Workflow: Finalización

## Regla Principal

**6 pasos en orden. Cada uno espera "si" para continuar.**

---

## Validación

Verificar EXECUTE completado en sesión.

Si no completado → Error: "Completa EXECUTE primero"

---

## PASO 1: Commit

### 1a: Mostrar archivos modificados

```bash
git status --porcelain
```

```
PASO 1 DE 6: Commit

Archivos modificados:
- archivo1.py
- archivo2.py
```

### 1b: Esperar "si"

**Esperar "si" o "abort".**

### 1c: Commit

```bash
git add <archivos>
git commit -m "MCF-XXX: mensaje"
```

---

## PASO 2: Push

### 2a: Mostrar

```
PASO 2 DE 6: Push

Rama: feature/MCF-XXX-descripcion
```

### 2b: Esperar "si"

**Esperar "si" o "abort".**

### 2c: Push

```bash
git push --set-upstream origin feature/MCF-XXX-descripcion
```

---

## PASO 3: Verificar Commits

### 3a: Mostrar commits

```bash
git log origin/development..HEAD --oneline
```

```
PASO 3 DE 6: Verificar Commits

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

**Esperar "si" o "abort".**

---

## PASO 4: Crear PR

### 4a: Generar contenido

Título: `MCF-XXX: título de la tarea`

Descripción generada:
```
## Summary

- Cambio realizado
- Tests verificados

## Links

| Recurso | URL |
|---------|-----|
| YouTrack | https://communities.youtrack.cloud/issue/MCF-XXX |
```

### 4b: Mostrar preview

```
PASO 4 DE 6: Crear PR

Título: MCF-XXX: título
Base: development
Head: feature/MCF-XXX-descripcion
```

### 4c: Esperar "si"

**Esperar "si" o "abort".**

### 4d: Crear PR

```bash
gh pr create \
  --title "MCF-XXX: título" \
  --body "descripción" \
  --base development \
  --head feature/MCF-XXX-descripcion
```

Mostrar URL del PR.

---

## PASO 5: Comentar YouTrack

### 5a: Generar comentario

```
## PR Creado

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

**Esperar "si" o "abort".**

### 5c: Comentar

Usar `youtrack_add_issue_comment` con el texto generado.

---

## PASO 6: Merge

### 6a: Mostrar

```
PASO 6 DE 6: Merge

¿Hacemos merge del PR?
ADVERTENCIA: Esto mergea a development.
```

### 6b: Esperar "si"

**Esperar "si" o "no".**

### 6c: Si "si"

```bash
gh pr merge --squash
git push origin --delete feature/MCF-XXX-descripcion
git branch -d feature/MCF-XXX-descripcion
rm .context/session_*.md
```

### 6d: Si "no"

Mantener sesión.

---

## Resumen Final

```
================================================================
✅ WORKFLOW COMPLETADO
================================================================

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

Sesión eliminada.
================================================================
```

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
