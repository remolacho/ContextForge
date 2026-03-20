---
inclusion: manual
---

# Skill: Formato de Clases

Define el estándar para estructurar clases en ContextForge.

## Reglas

| Regla | Descripción |
|-------|-------------|
| 1 | Máximo **15 líneas** por método |
| 2 | Métodos privados con **≤10 palabras** de descripción |
| 3 | Públicos **primero**, privados **después** |
| 4 | Privados en **orden de ejecución**, no alfabético |
| 5 | Docstrings de **≤10 palabras** |
| 6 | NO **ifs anidados** ni complejidad alta |
| 7 | Bloques `for`/`if` complejos se extraen a **métodos privados** |

## Estructura

```
┌─────────────────────────────────┐
│ CLASE                           │
├─────────────────────────────────┤
│ Atributos                        │
│                                  │
│ ════════ ZONA PÚBLICA ════════ │
│ methods de API                  │
│                                  │
│ ════════ ZONA PRIVADA ════════  │
│ 1. _step_one()   # primer paso  │
│ 2. _step_two()   # segundo paso │
│ 3. _step_three() # tercer paso  │
└─────────────────────────────────┘
```

## Convenciones

| Tipo | Prefijo | Ubicación |
|------|---------|----------|
| Público | Ninguno | Zona pública |
| Privado | `_` | Zona privada |

## Separadores

```python
# ════════ ZONA PÚBLICA ════════

# ════════ ZONA PRIVADA ════════
```
