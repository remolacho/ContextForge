# Workflow: Ejecución

## Regla Principal

**Para cada paso del plan:**
1. Mostrar descripción
2. Esperar "next"
3. Ejecutar
4. make check
5. Actualizar sesión

---

## Validación

→ Leer `.agents/skills/workflow/validate_previous_step.md`

Si no completado → Error: "Completa PLAN primero"

---

## Leer sesión activa

→ Leer `.agents/skills/session/read.md`

Mostrar resumen de progreso.

---

## Ejecución de Pasos

### Para cada paso del plan:

#### 1. MOSTRAR descripción

```
============================================================
PASO N DE M: [nombre del paso]
============================================================

Descripción: ...
Archivos: ...

Reglas aplicables: .agents/rules/*.md
============================================================
```

→ Leer `.agents/skills/workflow/identify_rules.md`

#### 2. ESPERAR "next"

→ Leer `.agents/skills/workflow/wait_next.md`

#### 3. EJECUTAR

1. Ejecutar código
2. → Leer `.agents/skills/checks/make_check.md`
3. Reportar resultado

#### 4. Si FALLA

→ Leer `.agents/skills/workflow/wait_abort.md`

```
ERROR: make check FALLÓ

LINT: ...
TYPECHECK: ...
TESTS: ...

Esperar "retry" o "abort".
```

#### 5. Si PASA

→ Leer `.agents/skills/session/update.md`

Marcar paso completado en sesión.

---

## Verificación Final

Después de completar todos los pasos:

→ Leer `.agents/skills/checks/make_check.md`

Mostrar resultados.

---

## Continuar

→ Leer `.agents/skills/workflow/wait_next.md`

→ Leer `finalize_workflow.md`

---

## Comandos

| Comando | Qué |
|---------|-----|
| make check | lint + typecheck + test |
| next | Siguiente paso |
| abort | Detener |
| retry | Reintentar make check |
