# Workflow: Finalización

## Pasos

### 1. Squash Commits

- Ejecutar: `git reset --soft $(git merge-base HEAD origin/<base>)`
- Crear UN solo commit
- Usar mensaje según `.agents/templates/commit_template.md`
- Formato: `{MCF-XXX}: descripción corta`

### 2. Push

- Ejecutar: `git push --force-with-lease`

### 3. Crear PR

- Usar herramienta `gh pr create`
- Usar `.agents/templates/pr_template.md`
- Título incluye ID de tarea
- Body con: Summary, Changes, Verification, Links

### 4. Agregar comentario en YouTrack

- Usar herramienta `youtrack_add_issue_comment`
- Agregar link del PR y validación:
  - Lint: passed
  - Typecheck: passed
  - Tests: X passed
- **NO modificar la descripción de la tarea**

### 5. Merge (opcional)

- Preguntar: "¿Quieres cerrar la rama y hacer merge?"
- Si confirma:
  - `gh pr merge`
  - Eliminar rama feature
  - **Actualizar estado YouTrack a "Hecho" (Fixed/Done)**
  - Usar herramienta `youtrack_update_issue`
  - Cambiar estado a "Hecho" o "Fixed"

## Confirmaciones

| Paso | Pregunta | Respuesta |
|------|----------|-----------|
| Commit | "¿Hacemos el commit?" | "si" / "no" |
| Push | "¿Hacemos push?" | "si" / "no" |
| PR | "¿Creamos el PR?" | "si" / "no" |
| YouTrack | "¿Actualizamos YouTrack?" | "si" / "no" |
| Merge | "¿Quieres hacer merge?" | "si" / "no" |

## Flujo Completo

```
1. Commit → 2. Push → 3. PR → 4. YouTrack → 5. Merge (opcional)
```

Cada paso requiere confirmación antes de ejecutar.
