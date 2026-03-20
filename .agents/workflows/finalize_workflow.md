# Workflow: Finalización

## Regla Principal

**Cada paso requiere confirmación explícita antes de ejecutar. NO continuar sin esperar respuesta.**
**Este workflow es OBLIGATORIO al terminar la ejecución de una tarea.**
**El archivo de sesión se actualiza y elimina después de merge exitoso.**

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
================================================================
FINALIZACIÓN DE SESIÓN
================================================================
Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion
PR: (pendiente)

Pasos restantes:
[ ] 1. Commit (squash)
[ ] 2. Push
[ ] 3. Crear PR
[ ] 4. Comentar en YouTrack
[ ] 5. Merge (opcional)
================================================================
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

## Checklist de Pasos (en orden obligatorio)

```
[ ] 1. Commit (squash) - obligatorio
[ ] 2. Push - obligatorio
[ ] 3. Crear PR - obligatorio
[ ] 4. Comentar en YouTrack - obligatorio
[ ] 5. Merge - opcional (solicitar confirmación)
```

---

## PASO 1: Commit (Squash)

### 1a: Mostrar estado de commits

```
================================================================
PASO 1 DE 5: Commit (Squash)
================================================================

Commits en esta rama (desde base):
- abc1234: Initial commit
- def5678: Add ContextItemBuilder
- ghi9012: Add tests

Total: 3 commits (serán squash en 1)
```

---

### 1b: Solicitar confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR respuesta.

```
¿Hacemos squash y commit? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a ejecutar squash |
| "no" | Saltar a PASO 2 |
| "abort" | Abortar seluruh workflow |

---

### 1c: Ejecutar squash

```bash
git merge-base HEAD origin/development
# o para hotfix:
# git merge-base HEAD origin/main
```

```bash
git reset --soft $(git merge-base HEAD origin/development)
```

---

### 1d: Leer template de commit

- Leer `.agents/templates/commit_template.md`
- Generar mensaje de commit

---

### 1e: Solicitar confirmación del mensaje

```
Mensaje de commit propuesto:

MCF-XXX: descripción corta de la tarea

¿Confirmamos este mensaje? (si/no/modificar)
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Ejecutar commit |
| "modificar" | Solicitar nuevo mensaje |
| "no" | Cancelar commit, volver a espera |

---

### 1f: Ejecutar commit

```bash
git commit -m "MCF-XXX: mensaje"
```

---

### 1g: Actualizar sesión después de commit

```markdown
### FINALIZE
- [x] Commit
- [ ] Push
- [ ] Crear PR
- [ ] Comentar en YouTrack
- [ ] Merge
```

---

## PASO 2: Push

### 2a: Solicitar confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR respuesta.

```
¿Hacemos push? (si/no)

Rama: feature/MCF-XXX-descripcion
Remote: origin
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a ejecutar push |
| "no" | Saltar a PASO 3 |

---

### 2b: Ejecutar push

```bash
git push --set-upstream origin feature/MCF-XXX-descripcion
```

---

### 2c: Actualizar sesión después de push

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [ ] Crear PR
- [ ] Comentar en YouTrack
- [ ] Merge
```

---

## PASO 3: Crear Pull Request

### 3a: Solicitar confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR respuesta.

```
¿Creamos el Pull Request? (si/no)

Base: development (feature) / main (hotfix)
Head: feature/MCF-XXX-descripcion
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a crear PR |
| "no" | Saltar a PASO 4 |

---

### 3b: Leer template de PR

- Leer `.agents/templates/pr_template.md`

---

### 3c: Generar PR

Usar herramienta `gh pr create`:

```bash
gh pr create \
  --title "MCF-XXX: título de la tarea" \
  --body "$(cat .agents/templates/pr_template.md)" \
  --base development \
  --head feature/MCF-XXX-descripcion
```

---

### 3d: Mostrar resultado

```
================================================================
Pull Request creado:
https://github.com/.../pull/N

Base: development
Commits: 1 (squash)
================================================================
```

---

### 3e: Actualizar sesión después de crear PR

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [x] Crear PR
- [ ] Comentar en YouTrack
- [ ] Merge

## Notas

PR: https://github.com/.../pull/N
```

---

## PASO 4: Actualizar YouTrack

### 4a: Solicitar confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR respuesta.

```
¿Agregamos comentario en YouTrack con el link del PR? (si/no)

MCF-XXX: https://communities.youtrack.cloud/issue/MCF-XXX
PR: https://github.com/.../pull/N
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a agregar comentario |
| "no" | Saltar a PASO 5 |

---

### 4b: Agregar comentario

Usar herramienta `youtrack_add_issue_comment`:

```markdown
## PR Creado

PR: {URL_DEL_PR}

## Verificaciones

| Verificación | Estado |
|-------------|--------|
| Lint (`make lint`) | ✅ passed |
| Typecheck (`make typecheck`) | ✅ passed |
| Tests (`make test`) | ✅ N passed |
```

**NOTA:** NO modificar la descripción de la tarea.

---

### 4c: Actualizar sesión después de comentar

```markdown
### FINALIZE
- [x] Commit
- [x] Push
- [x] Crear PR
- [x] Comentar en YouTrack
- [ ] Merge
```

---

## PASO 5: Merge (opcional)

### 5a: Solicitar confirmación

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR respuesta.

```
¿Hacemos merge del PR? (si/no)

ADVERTENCIA: Esto mergea a development/main.
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a ejecutar merge |
| "no" | Ir a RESUMEN FINAL |

---

### 5b: Ejecutar merge

```bash
gh pr merge --squash
```

---

### 5c: Eliminar rama feature

```bash
git push origin --delete feature/MCF-XXX-descripcion
git branch -d feature/MCF-XXX-descripcion
```

---

### 5d: Eliminar archivo de sesión

```bash
rm .context/session_*.md
```

---

### 5e: Actualizar estado final

```
================================================================
SESIÓN ELIMINADA
================================================================
Tarea: MCF-XXX ✅
Rama: feature/MCF-XXX-descripcion (eliminada)
PR: mergeado ✅
Sesión: eliminada ✅
================================================================
```

---

## RESUMEN FINAL (si no se hace merge)

```
================================================================
WORKFLOW DE FINALIZACIÓN
================================================================

Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion
PR: https://github.com/.../pull/N

Pasos completados:
[x] Commit
[x] Push
[x] Crear PR
[x] Comentar en YouTrack
[ ] Merge (pendiente)

Sesión guardada en: .context/session_*.md

Cuando estés listo para merge, responde 'finalize' de nuevo.

================================================================
```

---

## Estados de Espera

| Paso | ¿Espera? | Qué espera |
|------|----------|------------|
| Commit | **SÍ** | "si" / "no" / "abort" |
| Mensaje | **SÍ** | "si" / "modificar" / "no" |
| Push | **SÍ** | "si" / "no" |
| PR | **SÍ** | "si" / "no" |
| YouTrack | **SÍ** | "si" / "no" |
| Merge | **SÍ** | "si" / "no" |

---

## Manejo de Abort

Si el usuario responde "abort" en cualquier paso:
1. Mostrar que el workflow fue detenido
2. NO ejecutar ningún paso pendiente
3. Dejar los cambios en el estado actual
4. Sesión queda pausada para continuar después

---

## Reanudar Finalización

Si el usuario inicia `start` y hay sesión activa con FINALIZE incompleto:

```
================================================================
SESIÓN ACTIVA ENCONTRADA
================================================================
Tarea: MCF-XXX
Flujo: FINALIZE

Pasos restantes:
[ ] Merge

¿Deseas retomar? (si/no)
================================================================
```

| Respuesta | Acción |
|-----------|--------|
| "si" | Leer session_*.md, continuar desde donde quedó |
| "no" | Volver al inicio |

---

## Nota sobre Workflows de Agentes

Este workflow está diseñado para agentes. Al iniciar con `start`:
1. Buscar `.context/session_*.md`
2. Si existe y FINALIZE está incompleto → ofrecer retomar
3. Si no existe o FINALIZE completo → iniciar nueva sesión
