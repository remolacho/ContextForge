# Sesión: ContextForge

## Metadatos

| Campo | Valor |
|-------|-------|
| Fecha | {YYYY-MM-DD} |
| Hora | {HH:MM:SS} |
| Iniciado por | start |

---

## Flujo Principal

| Paso | Estado | Descripción |
|------|--------|-------------|
| 1. start | ⏳ | Buscar/Crear sesión |
| 2. INIT | ⏳ | Mostrar rol, reglas |
| 3. TASK_SOURCE | ⏳ | Fuente de tarea |
| 3a | ⏳ | Crear tarea en YouTrack (si es Archivo) |
| 4. Tipo_rama | ⏳ | Solicitar tipo de rama |
| 5. PLAN | ⏳ | Generar plan |
| 6. EXECUTE | ⏳ | Ejecutar pasos |
| 7. FINALIZE | ⏳ | Commit/Push/PR |

---

## Datos de Tarea

| Campo | Valor | Validado |
|-------|-------|----------|
| Fuente | Archivo / YouTrack | ⏳ |
| YouTrack Issue | MCF-XXX | ⏳ |
| Tipo de rama | feature / hotfix | ⏳ |
| Rama base | development / main | ⏳ |
| **Rama nombre** | feature/MCF-XXX-descripcion | ⏳ |

---

## Validación de Rama ⚠️ CRÍTICO

**ANTES de continuar de PLAN a EXECUTE, verificar:**

```bash
git branch --show-current
```

| Check | Comando | Esperado |
|-------|---------|----------|
| Rama existe | `git branch --show-current` | feature/MCF-XXX-... |
| Formato válido | regex match | feature/... o hotfix/... |
| Working dir limpio | `git status --porcelain` | vacío |

**Solo marcar PLAN como ✅ cuando rama esté validada.**

---

## Ejecución - Detalle

### PLAN
- [ ] Leer plan_workflow.md
- [ ] Extraer contexto de tasks.md
- [ ] Generar plan
- [ ] Mostrar plan
- [ ] Crear rama (git checkout -b ...)
- [ ] **Validar rama**
- [ ] Actualizar YouTrack (En curso)
- [ ] Esperar "next"

### EXECUTE
- [ ] Leer execute_workflow.md
- [ ] **Validar rama antes de iniciar**
- [ ] Paso 1: ...
- [ ] Paso 2: ...
- [ ] make check
- [ ] Esperar "next"

### FINALIZE
- [ ] **make check obligatorio**
- [ ] 1. Commit
- [ ] 2. Push
- [ ] 3. Verificar commits
- [ ] 4. Crear PR
- [ ] 5. Comentar YouTrack
- [ ] 6. Merge
- [ ] 7. YouTrack Done

---

## Notas

```
(espacio para notas de la sesión)
```

---

## Ultima actualización

Paso: ...
Hora: ...
