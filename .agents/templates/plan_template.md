# Plan de Implementación

---

## Header

| Campo | Valor |
|-------|-------|
| **Tarea** | {título de la tarea} |
| **ID** | {MCF-XXX} |
| **Rama** | {feature/MCF-XXX-descripcion} |
| **Skill** | {skill-aplicable.md} |
| **YouTrack** | https://communities.youtrack.cloud/issue/{MCF-XXX} |

---

## Descripción de la Tarea

{descripción completa extraída de tasks.md, incluyendo subtareas}

---

## Pasos de Implementación

| # | Descripción | Archivos | Skill |
|---|-------------|----------|-------|
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

---

## Detalle por Paso

### Paso 1: {nombre del paso}

**Descripción:** {descripción detallada}

**Archivos:**
| Acción | Ruta |
|--------|------|
| CREAR | `src/...` |
| MODIFICAR | `src/...` |

**Skill:** {skill aplicable}

---

### Paso 2: {nombre del paso}

**Descripción:** ...

---

## Archivos a Crear/Modificar

### Crear
- `src/infrastructure/builders/context_item.py`
- `src/infrastructure/builders/cache_entry.py`

### Modificar
- `src/domain/entities.py`
- `tests/unit/...`

---

## Verificación

### make check
```bash
make lint      # ruff check
make typecheck # mypy
make test      # pytest
make check     # todos
```

---

## Confirmación

**Responde "next" para iniciar la ejecución.**

```
=================================================================
¿Iniciamos la ejecución paso a paso?
Responde 'next' para continuar.
=================================================================
```

---

## Notas

- Rama base: {development / main}
- Tipo: {feature / hotfix}
- Workflow: execute_workflow.md
