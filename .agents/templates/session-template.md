# Sesión: {TAREA}
Fecha: {FECHA}
Hora: {HORA}
Rama: {RAMA}

## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ⏳ | No iniciado |
| TASK_SOURCE | ⏳ | No iniciado |
| PLAN | ⏳ | No iniciado |
| EXECUTE | ⏳ | No iniciado |
| FINALIZE | ⏳ | No iniciado |

## Progreso

### INIT
- [ ] Mostrar rol
- [ ] Listar skills
- [ ] Mostrar workflows
- [ ] Solicitar fuente de tarea

### TASK_SOURCE
- [ ] Solicitar fuente ("Archivo" o "YouTrack")
- [ ] Obtener información de tarea
- [ ] Crear tarea en YouTrack (si es flujo Archivo)
- [ ] Solicitar tipo de rama

### PLAN
- [ ] Leer plan_workflow.md
- [ ] Generar plan
- [ ] Solicitar confirmación

### EXECUTE
- [ ] Leer execute_workflow.md
- [ ] Ejecutar pasos
  - [ ] Paso 1
  - [ ] Paso 2
  - [ ] Paso 3
- [ ] Verificación final

### FINALIZE
- [ ] Leer finalize_workflow.md
- [ ] Commit
- [ ] Push
- [ ] Crear PR
- [ ] Comentar en YouTrack
- [ ] Solicitar merge

## Notas

```
(espacio para notas de la sesión)
```
