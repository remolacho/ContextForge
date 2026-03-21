# Workflow: Finalización

## Regla Principal

**Cada paso requiere confirmación explícita antes de ejecutar. NO continuar sin esperar respuesta.**
**Este workflow es OBLIGATORIO al terminar la ejecución de una tarea.**
**Squash se hace vía GitHub (no usar `git reset --soft`).**

---

## Validación de Sesión

### Verificar EXECUTE completado

Antes de iniciar, verificar en sesión:

```markdown
| Flujo | Estado |
|-------|--------|
| EXECUTE | ✅ |
| FINALIZE | 🔄 |
```

Si EXECUTE no está completado → Error: "Completa EXECUTE primero"

---

## Preparación Inicial

### Leer sesión activa

```bash
ls -la .context/session_*.md | tail -1
```

Mostrar resumen:
```
============================================================
FINALIZACIÓN DE SESIÓN
============================================================
Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion

Flujo completo:
[ ] 1. Commit
[ ] 2. Push
[ ] 3. Verificar commits (squash si necesario)
[ ] 4. Crear PR
[ ] 5. Comentar YouTrack
[ ] 6. Merge (opcional)
============================================================
```

---

## Actualizar sesión al iniciar FINALIZE

```markdown
## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | ✅ | Completado |
| PLAN | ✅ | Completado |
| EXECUTE | ✅ | Completado |
| FINALIZE | 🔄 | En progreso |
```

---

## PASO 1: Commit

### 1a: Mostrar archivos modificados

Ejecutar:
```bash
git status --porcelain
```

Mostrar solo archivos relevantes (excluir archivos de otros features):
```
============================================================
PASO 1 DE 6: Commit
============================================================

Archivos modificados/nuevos:
- archivo1.py
- archivo2.py

¿Incluir estos archivos en el commit?
```

---

### 1b: Solicitar confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR respuesta.

```
¿Hacemos commit de estos archivos? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a 1c |
| "no" | Solicitar cuáles archivos incluir |
| "abort" | Abortar gesamten workflow |

---

### 1c: Leer template de commit

- Leer `.agents/templates/commit_template.md`
- Leer sesión activa para obtener:
  - ID de tarea (MCF-XXX)
  - Descripción de lo realizado en EXECUTE

---

### 1d: Generar y confirmar mensaje

Mostrar mensaje propuesto:
```
Mensaje de commit propuesto:

MCF-XXX: descripción corta de la tarea

- Cambio 1 realizado en EXECUTE
- Cambio 2 realizado en EXECUTE
- Tests agregados/verificados
```

**ACCIÓN REQUERIDA:** ESPERAR respuesta.

```
¿Confirmamos este mensaje? (si/no/modificar)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a 1e |
| "modificar" | Solicitar nuevo mensaje |
| "no" | Cancelar, volver a espera |

---

### 1e: Ejecutar commit

```bash
git add <archivos_confirmados>
git commit -m "MCF-XXX: mensaje"
```

---

### 1f: Actualizar sesión

```markdown
### FINALIZE
- [x] Commit (hash)
- [ ] Push
- [ ] Verificar commits
- [ ] Crear PR
- [ ] Comentar YouTrack
- [ ] Merge
```

---

## PASO 2: Push

### 2a: Solicitar confirmación

```
============================================================
PASO 2 DE 6: Push
============================================================

¿Hacemos push? (si/no)

Rama: feature/MCF-XXX-descripcion
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a 2b |
| "no" | Abortar gesamten workflow |

---

### 2b: Ejecutar push

```bash
git push --set-upstream origin feature/MCF-XXX-descripcion
```

---

### 2c: Actualizar sesión

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [ ] Verificar commits
- [ ] Crear PR
- [ ] Comentar YouTrack
- [ ] Merge
```

---

## PASO 3: Verificar Commits

### 3a: Mostrar commits

```bash
git log origin/development..HEAD --oneline
```

```
============================================================
PASO 3 DE 6: Verificar Commits
============================================================

Commits desde origin/development:
- abc1234: Mensaje del commit 1
- def5678: Mensaje del commit 2
- ghi9012: Mensaje del commit 3

Total: N commits
```

---

### 3b: Verificar si hay más de 1 commit

**SI solo hay 1 commit:**
```
✅ Solo 1 commit - listo para PR
```
→ Ir directamente a PASO 4

**SI hay más de 1 commit:**
```
⚠️ IMPORTANTE: Los PR deben tener un solo commit.

Opciones:
1. Squash automático vía GitHub (recomendado)
2. Crear nueva rama limpia desde development
```

---

### 3c: Solicitar acción si hay múltiples commits

```
¿Quieres hacer squash de los commits? (si/no)

Opción 1 (si): Squash automático vía GitHub al crear PR
Opción 2 (no): Continuar con múltiples commits (no recomendado)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a PASO 4 (GitHub hará squash automático) |
| "no" | ADVERTENCIA: PR tendrá múltiples commits |

---

### 3d: Actualizar sesión

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [x] Verificar commits (N commits, squash vía GitHub)
- [ ] Crear PR
- [ ] Comentar YouTrack
- [ ] Merge
```

---

## PASO 4: Crear PR

### 4a: Generar contenido del PR

**Fuentes:**
- Leer `.agents/templates/pr_template.md`
- Leer sesión activa para extraer:
  - ID de tarea
  - Descripción de EXECUTE
  - Archivos modificados

**Título:**
```
MCF-XXX: título de la tarea
```

**Descripción (generada dinámicamente):**
```
## Summary

- [punto 1 de lo realizado]
- [punto 2 de lo realizado]
- Tests agregados/verificados

## Changes

| Tipo | Archivos |
|------|----------|
| Creados | archivo1.py |
| Modificados | archivo2.py |

## Verification

| Verificación | Estado |
|--------------|--------|
| Lint (`make lint`) | ✅ passed |
| Typecheck (`make typecheck`) | ✅ passed |
| Tests (`make test`) | ✅ passed |

## Links

| Recurso | URL |
|---------|-----|
| YouTrack | https://communities.youtrack.cloud/issue/MCF-XXX |
| Sprint | https://communities.youtrack.cloud/agiles/195-1/current |
```

---

### 4b: Mostrar PR preview

```
============================================================
PASO 4 DE 6: Crear PR
============================================================

Título:
MCF-XXX: descripción de la tarea

Descripción:
---
[descripción generada arriba]
---

Archivos:
- archivo1.py
- archivo2.py

Commits: N (serán squash a 1 por GitHub)

Base: development
Head: feature/MCF-XXX-descripcion
```

---

### 4c: Solicitar confirmación

**ACCIÓN REQUERIDA:** ESPERAR respuesta.

```
¿Creamos el Pull Request con esta información? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a 4d |
| "no" | Solicitar modificaciones |

---

### 4d: Ejecutar PR

```bash
gh pr create \
  --title "MCF-XXX: título de la tarea" \
  --body "contenido de la descripción" \
  --base development \
  --head feature/MCF-XXX-descripcion
```

---

### 4e: Mostrar resultado

```
============================================================
✅ Pull Request creado exitosamente
============================================================

URL: https://github.com/remolacho/ContextForge/pull/N
Base: development
Head: feature/MCF-XXX-descripcion
Commits: N → 1 (squash automático por GitHub)
```

---

### 4f: Actualizar sesión

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [x] Verificar commits
- [x] Crear PR: https://github.com/.../pull/N
- [ ] Comentar YouTrack
- [ ] Merge
```

---

## PASO 5: Comentar en YouTrack

### 5a: Generar checklist de verificación

**Fuentes:**
- Leer sesión activa → extraer lo realizado en EXECUTE
- Leer `.kiro/specs/contextforge/tasks.md` → extraer subtareas de la tarea

```
============================================================
PASO 5 DE 6: Comentar en YouTrack
============================================================

MCF-XXX: https://communities.youtrack.cloud/issue/MCF-XXX
PR: https://github.com/remolacho/ContextForge/pull/N
```

---

### 5b: Generar comentario

```
## PR Creado

PR: {URL_DEL_PR}

## Resumen de Cambios

- [x] Cambio 1 realizado
- [x] Cambio 2 realizado
- [x] Tests agregados/verificados

## Verificación

| Verificación | Estado |
|-------------|--------|
| Lint (`make lint`) | ✅ passed |
| Typecheck (`make typecheck`) | ✅ passed |
| Tests (`make test`) | ✅ passed |

## Checklist de Tarea

| Subtarea | Estado |
|----------|--------|
| Subtarea 1.1 | ✅ completada |
| Subtarea 1.2 | ✅ completada |

---

⚠️ ¿Se cumplen todos los criterios de la tarea?
```

---

### 5c: Solicitar confirmación

**ACCIÓN REQUERIDA:** ESPERAR respuesta.

```
¿Agregamos este comentario en YouTrack? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a 5d |
| "no" | Ir a RESUMEN FINAL |

---

### 5d: Ejecutar comentario

Usar herramienta `youtrack_add_issue_comment`:
- Issue ID: MCF-XXX
- Texto: comentario generado en 5b

---

### 5e: Actualizar sesión

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [x] Verificar commits
- [x] Crear PR
- [x] Comentar YouTrack
- [ ] Merge
```

---

## PASO 6: Merge (opcional)

### 6a: Solicitar confirmación

```
============================================================
PASO 6 DE 6: Merge (opcional)
============================================================

¿Hacemos merge del PR? (si/no)

ADVERTENCIA: Esto mergea a development/main.
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a 6b |
| "no" | Ir a RESUMEN FINAL |

---

### 6b: Ejecutar merge

```bash
gh pr merge --squash
```

---

### 6c: Eliminar rama feature

```bash
git push origin --delete feature/MCF-XXX-descripcion
git branch -d feature/MCF-XXX-descripcion
```

---

### 6d: Eliminar archivo de sesión

```bash
rm .context/session_*.md
```

---

## RESUMEN FINAL

```
============================================================
✅ WORKFLOW DE FINALIZACIÓN COMPLETADO
============================================================

Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion (eliminada)
PR: https://github.com/remolacho/ContextForge/pull/N (mergeado ✅)
YouTrack: comentado ✅

Sesión eliminada.
============================================================
```

---

## RESUMEN FINAL (sin merge)

```
============================================================
FINALIZACIÓN PAUSADA
============================================================

Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion
PR: https://github.com/remolacho/ContextForge/pull/N

Pasos completados:
[x] Commit
[x] Push
[x] Verificar commits
[x] Crear PR
[x] Comentar YouTrack

Pendiente:
[ ] Merge (responde 'merge' cuando estés listo)

Sesión guardada en: .context/session_*.md
============================================================
```

---

## Estados de Espera

| Paso | ¿Espera? | Qué espera |
|------|----------|------------|
| 1. Commit | **SÍ** | "si" / "no" / "abort" |
| 2. Push | **SÍ** | "si" / "no" |
| 3. Commits | **SÍ** | "si" / "no" |
| 4. PR | **SÍ** | "si" / "no" |
| 5. YouTrack | **SÍ** | "si" / "no" |
| 6. Merge | **SÍ** | "si" / "no" |

---

## Reglas de Seguridad

### ❌ NUNCA hacer
- `git reset --soft` (borra historial y puede perder cambios)
- `git reset --hard` (pierde cambios no commiteados)

### ✅ SQUASH SEGURO
El squash se hace automáticamente por GitHub al hacer merge con `--squash`.

---

## Reanudar Finalización

Si el usuario inicia `start` y hay sesión activa con FINALIZE incompleto:

```
============================================================
SESIÓN ACTIVA ENCONTRADA
============================================================
Tarea: MCF-XXX
Flujo: FINALIZE

Pasos restantes:
[ ] Merge

¿Deseas retomar? (si/no)
============================================================
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Leer session_*.md, continuar desde donde quedó |
| "no" | Volver al inicio |
