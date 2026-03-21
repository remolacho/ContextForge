# Workflow: Inicialización

## Validación Previa

→ Leer `.agents/skills/session/read.md`

Verificar:
| Check | Si existe | Si no existe |
|-------|-----------|--------------|
| Sesión | Mostrar resumen, esperar "retomar"/"nueva" | Crear nueva |

---

## Paso 1: Buscar sesión

→ Leer `.agents/skills/session/read.md`

---

## Paso 2: Mostrar rol

→ Leer `.agents/prompts/role.md`

```
ROL: Desarrollador Senior Python

Habilidades:
- Clean Architecture y patrones de diseño
- LangChain y LCEL
- Testing con pytest y hypothesis
- Docker y DevOps
- Gestión de proyectos con YouTrack
```

---

## Paso 3: Listar reglas de desarrollo

| Regla de Desarrollo | Descripción |
|-------|-------------|
| `.agents/rules/class_format.md` | Formato de clases (≤15 líneas/método) |
| `.agents/rules/controllers.md` | Patrón FastAPI controllers |
| `.agents/rules/factories.md` | Patrón Factory |
| `.agents/rules/domain_layer.md` | Entidades, interfaces, excepciones |
| `.agents/rules/builders.md` | ContextItemBuilder, CacheEntryBuilder |
| `.agents/rules/providers.md` | YouTrackProvider, ProviderFactory |
| `.agents/rules/cache.md` | ChromaCacheRepository |
| `.agents/rules/llm.md` | GeminiLLMEngine, Summarized |

---

## Paso 4: Listar workflows

→ Leer `.agents/skills/workflow/read_workflow.md`

- init_workflow.md — Inicialización
- task_source_workflow.md — Fuente de tareas
- plan_workflow.md — Planificación
- execute_workflow.md — Ejecución
- finalize_workflow.md — Finalización

---

## Paso 5: Crear sesión

→ Leer `.agents/skills/session/create.md`

---

## Validación INIT Completado

Antes de continuar a TASK_SOURCE, verificar:

| Check | Estado |
|-------|--------|
| Sesión creada | .context/session_*.md existe |
| Rol mostrado | ✅ |
| Reglas listadas | ✅ |
| Workflows listados | ✅ |

**Si todo correcto:**
```
✅ INIT completado.
Continuando a TASK_SOURCE...
```

→ Leer `.agents/skills/session/update.md`

Actualizar sesión:
```markdown
| 2. INIT | ✅ | Mostrar rol, reglas |
```

---

## Continuar

→ Leer `task_source_workflow.md`
