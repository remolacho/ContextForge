# Generate Plan

## Description
Generate implementation plan based on task requirements.

## Input
- Task description from source
- Requirements from `.agents/docs/init_proyect/requirements.md`
- Applicable rules from `.agents/rules/*.md`

## Output Format
Use `plan_template.md` structure:

```markdown
# Plan de Implementación

## Header
| Campo | Valor |
|-------|-------|
| Tarea | {title} |
| ID | {MCF-XXX} |
| Rama | {branch} |
| Regla | {rule-file} |

## Pasos de Implementación
| # | Descripción | Archivos | Regla |
|---|-------------|----------|-------|
| 1 | ... | ... | ... |

## Detalle por Paso
### Paso 1: {name}
- Descripción
- Archivos a crear/modificar
```

## Next Step
Return to invoking workflow
