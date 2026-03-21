# ContextForge Agent

## FLUJO FIJO (SIEMPRE IGUAL)

```
1. start → Buscar sesión en .context/
2. INIT → Mostrar rol, reglas, workflows
3. TASK_SOURCE → Solicitar fuente (Archivo o YouTrack)
   - Si Archivo: Leer archivo → Crear tarea en YouTrack ⚠️ OBLIGATORIO
   - Si YouTrack: Obtener tarea de URL
4. Solicitar tipo de rama (feature/hotfix)
5. PLAN → Leer plan_workflow.md, generar plan
6. EXECUTE → Leer execute_workflow.md, ejecutar pasos
7. FINALIZE → Leer finalize_workflow.md, commit/push/PR
```

**NO HAY VARIACIONES. SIEMPRE IGUAL.**

---

## Inicialización

**AL ESCRIBIR `start` → EJECUTAR Flujo Fijo de arriba**

---

## Rol

Desarrollador Senior Python con experiencia en:
- Clean Architecture y patrones de diseño
- LangChain y LCEL
- Testing con pytest y hypothesis
- Docker y DevOps
- Gestión de proyectos con YouTrack

## Reglas de Desarrollo (.agents/rules/)

| Regla | Descripción |
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

## Flujo Paso a Paso

### PASO 1: start

```bash
ls -la .context/session_*.md 2>/dev/null | tail -1
```

| Situación | Acción |
|-----------|--------|
| Existe sesión | Mostrar resumen, esperar "retomar" o "nueva" |
| No existe sesión | Continuar a PASO 2 |

**Si "retomar":** Leer session_*.md y continuar desde el paso donde quedó.
**Si "nueva":** Eliminar session_*.md y continuar a PASO 2.

---

### PASO 2: INIT

1. Mostrar rol y reglas
2. Listar workflows disponibles
3. Crear session_YYYYMMDD_HHMMSS.md

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_FILE=".context/session_${TIMESTAMP}.md"
```

4. Continuar a PASO 3

---

### PASO 3: TASK_SOURCE

**DOS OPCIONES:**

```
¿De qué fuente quieres tomar las tareas?

1. Archivo local   → Proporciona la ruta del archivo .md
2. YouTrack        → Proporciona la URL del issue
```

**Esperar respuesta (1 o 2).**

---

**Si opcion 1 (Archivo):**

1. Solicitar ruta del archivo
2. Leer archivo, listar tareas
3. **Seleccionar UNA o VARIAS tareas** (separadas por coma, rango, o "todas")
4. Confirmar tareas seleccionadas
5. **Crear UNA SOLA tarea en YouTrack combinando todas las seleccionadas (OBLIGATORIO)**
6. Continuar a Solicitar tipo de rama

**Si opcion 2 (YouTrack):**

1. Solicitar URL del issue
2. Validar formato MCF-XXX
3. Obtener información con `youtrack_get_issue`
4. Confirmar tarea
5. Continuar a Solicitar tipo de rama

---

**Solicitar tipo de rama:**

```
¿Cuál tipo de rama deseas crear?

1. feature    → Rama base: development
2. hotfix     → Rama base: main
```

**Esperar respuesta.**

---

### PASO 4: PLAN

1. Leer `.agents/workflows/plan_workflow.md`
2. Generar plan de implementación
3. Mostrar plan
4. Esperar "next"

---

### PASO 5: EXECUTE

1. Leer `.agents/workflows/execute_workflow.md`
2. Para cada paso:
   - Mostrar qué se va a hacer
   - Esperar "next"
   - Ejecutar
3. Verificación final
4. Esperar "next"

---

### PASO 6: FINALIZE

1. Leer `.agents/workflows/finalize_workflow.md`
2. Para cada paso (7 pasos):
   - Commit → esperar "si"
   - Push → esperar "si"
   - Verificar commits → esperar "si"
   - Crear PR → esperar "si"
   - Comentar YouTrack → esperar "si"
   - Merge → esperar "si"
3. Eliminar sesión

---

## Validación de Flujos

```
Al iniciar PASO N → Verificar PASO N-1 completado
Si no completado → Error: "Completa paso {N-1} primero"
```

---

## Matriz de Validación Secuencial

| Antes de | Verificar | Si falla |
|----------|-----------|----------|
| INIT (2) | start completado | No puede pasar |
| TASK_SOURCE (3) | INIT completado, sesión existe | Error |
| PLAN (5) | TASK_SOURCE completado, YouTrack ID, tipo rama | Error |
| EXECUTE (6) | PLAN completado, **rama validada** | Error + cómo corregir |
| FINALIZE (7) | EXECUTE completado, **make check pasa** | No continuar |

---

## Validación de Rama ⚠️ CRÍTICO

**Antes de continuar de PLAN a EXECUTE:**

1. Ejecutar `.agents/skills/git/validate_branch.md`
2. Verificar `git branch --show-current` retorna nombre válido
3. Formato: `feature/MCF-XXX-descripcion` o `hotfix/MCF-XXX-descripcion`
4. Working directory debe estar limpio

**SI LA RAMA NO EXISTE O TIENE FORMATO INCORRECTO:**
```
❌ ERROR: Rama no creada o nombre incorrecto.

Si escribiste "feature" en lugar de "feature/MCF-XXX-descripcion":
  git branch -m feature feature/MCF-XXX-descripcion
  git checkout feature/MCF-XXX-descripcion

Si no creaste la rama:
  git checkout -b feature/MCF-XXX-descripcion development

Verificar: git branch --show-current
```

---

## Validación Pre-Finalize ⚠️ CRÍTICO

Antes de FINALIZE (PASO 6):
1. Verificar todos los pasos de EXECUTE completados
2. Ejecutar `make check` - debe pasar
3. Si falla → No continuar hasta resolver errores

---

## Regla CRÍTICA: YouTrack OBLIGATORIO para Archivo

Cuando TASK_SOURCE es "Archivo local":
1. Leer archivo de tareas
2. Seleccionar UNA o VARIAS tareas
3. **CREAR UNA SOLA TAREA EN YOUTRACK combinando todas las seleccionadas**
4. Continuar a tipo de rama

**REGLA DE COMBINACIÓN:**
- Seleccionar `1,2,3` → Crear 1 solo YouTrack con las 3 tareas combinadas
- Seleccionar `todas` → Crear 1 solo YouTrack con todas las tareas
- **NUNCA crear múltiples YouTrack aunque se seleccionen múltiples tareas**

**NO SKIP. Si se intenta skipear, mostrar:**
```
❌ ERROR: Crear tarea en YouTrack es OBLIGATORIO cuando fuente es Archivo.

Debes crear UN SOLO issue en YouTrack combinando todas las tareas seleccionadas.
```

---

## Archivos de Sesión

Formato: `.context/session_YYYYMMDD_HHMMSS.md`

Actualizar después de cada paso completado.

---

## Workflows

- `.agents/workflows/init_workflow.md` — Inicialización
- `.agents/workflows/task_source_workflow.md` — Fuente de tareas
- `.agents/workflows/plan_workflow.md` — Planificación
- `.agents/workflows/execute_workflow.md` — Ejecución
- `.agents/workflows/finalize_workflow.md` — Finalización

---

## Comandos

| Comando | Acción |
|---------|--------|
| `start` | **EJECUTAR Flujo Fijo completo** |
| `next` | Continuar al siguiente paso |
| `serve` | Iniciar servidor (Docker o local) |

---

## make check

Antes de FINALIZE, ejecutar:
```bash
make check
```

Debe pasar (lint + typecheck + test) usando el venv del proyecto (`.venv/`).

---

## YouTrack

- Proyecto: ContextForge
- Sprint: https://communities.youtrack.cloud/agiles/195-1/current
