# Workflow: Finalización

## Pasos

1. **Squash commits**
   - `git reset --soft $(git merge-base HEAD origin/<base>)`
   - Un solo commit con mensaje descriptivo

2. **Push**
   - `git push --force-with-lease`

3. **Crear PR**
   - Usar `gh pr create`
   - Título incluye ID de tarea
   - Body con resumen y verificación

4. **Actualizar YouTrack**
   - **Sprint:** https://communities.youtrack.cloud/agiles/195-1/current
   - Usar `youtrack_update_issue`
   - Agregar link del PR
   - Agregar comentario con validación

5. **Merge (opcional)**
   - Preguntar: "¿Quieres cerrar la rama y hacer merge?"
   - Si confirma: `gh pr merge`
   - Eliminar rama feature
   - Cerrar tarea en YouTrack
