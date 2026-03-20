# Workflow: Fuente de Tareas

## Regla Principal

**Este workflow tiene DOS flujos separados: ARCHIVO y YOUTRACK.**
**Usar sesión activa en `.context/session_*.md` para tracking.**

---

## Paso 1: Leer sesión activa

```bash
ls -la .context/session_*.md | tail -1
```

Verificar que INIT está completado en la sesión:
```markdown
| Flujo | Estado |
|-------|--------|
| INIT | ✅ |
| TASK_SOURCE | 🔄 |
```

Si INIT no está completado → Error: "Completa INIT primero"

---

## Actualizar sesión al iniciar TASK_SOURCE

```markdown
## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | 🔄 | Solicitando fuente |
| PLAN | ⏳ | No iniciado |
| EXECUTE | ⏳ | No iniciado |
| FINALIZE | ⏳ | No iniciado |
```

---

# FLUJO: ARCHIVO LOCAL

## Paso 1: Solicitar ruta del archivo

**ACCIÓN REQUERIDA:** Mostrar pregunta y ESPERAR respuesta.

```
Proporciona la ruta al archivo de tareas (.md):
Ejemplo: .kiro/specs/contextforge/tasks.md
```

**PUNTOS DE ESPERA:**
| Situación | Acción |
|-----------|--------|
| Usuario da ruta | Verificar que existe |
| Archivo no existe | Mostrar error, solicitar ruta válida |
| Archivo no existe (2da vez) | Ofrecer cambiar a YouTrack |

---

## Paso 2: Verificar existencia

- Si la ruta NO existe → mostrar error y volver a Paso 1
- Si la ruta NO existe (intento 2+) → ofrecer cambiar a YouTrack
- Si la ruta existe → continuar a Paso 3

---

## Paso 3: Leer archivo

- Leer el archivo completo
- Parsear tareas del formato markdown con listas `- [ ]`
- Extraer: título, descripción, subtareas
- NO continuar hasta tener contenido válido

---

## Paso 4: Listar tareas disponibles

**ACCIÓN REQUERIDA:** Mostrar lista completa y ESPERAR número del usuario.

```
Tareas disponibles:

[1] Título tarea 1
[2] Título tarea 2
[3] Título tarea 3
...

¿Cuál tarea deseas tomar? (ingresa el número)
```

**PUNTOS DE ESPERA:**
| Situación | Acción |
|-----------|--------|
| Número válido (1-N) | Continuar a Paso 5 |
| Número inválido | Mostrar error, listar rango válido |
| Input no numérico | Mostrar error, solicitar número |

---

## Paso 5: Solicitar confirmación de tarea

Mostrar tarea seleccionada:
```
Tarea seleccionada:

[5] Implementar Infrastructure Layer: Factories

Descripción: ...
Subtareas: ...
```

**ACCIÓN REQUERIDA:** ESPERAR confirmación del usuario.

```
¿Deseas tomar esta tarea? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" / "sí" / "yes" | Continuar a Paso 6 |
| "no" | Volver a Paso 4 (mostrar lista) |
| Otra cosa | Solicitar "si" o "no" |

---

## Paso 6: Crear tarea en YouTrack

**SOLO ejecutar DESPUÉS de confirmación.**

- **Project:** ContextForge
- **Sprint:** https://communities.youtrack.cloud/agiles/195-1/current
- Usar herramienta `youtrack_create_issue`
- **IMPORTANTE:** Crear UNA sola tarea con TODO el contenido:
  - Título de la tarea seleccionada
  - Descripción completa preservada
  - Subtareas como lista en descripción
  - Preservar estructura y formato original

**Mostrar resultado:**
```
Tarea creada en YouTrack:
https://communities.youtrack.cloud/issue/MCF-XXX
```

---

## Actualizar sesión después de confirmar tarea

```markdown
### TASK_SOURCE
- [x] Solicitar fuente ("Archivo")
- [x] Leer archivo de tareas
- [x] Seleccionar tarea
- [x] Confirmar tarea
- [ ] Crear tarea en YouTrack

## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | 🔄 | Esperando tipo de rama |
| PLAN | ⏳ | No iniciado |
```

---

## Continuar a Solicitar tipo de rama

---

# FLUJO: YOUTRACK URL

## Paso 1: Solicitar URL de YouTrack

**ACCIÓN REQUERIDA:** Mostrar pregunta y ESPERAR respuesta.

```
Proporciona la URL del issue de YouTrack:
Ejemplo: https://communities.youtrack.cloud/issue/MCF-123
```

**PUNTOS DE ESPERA:**
| Situación | Acción |
|-----------|--------|
| Usuario da URL | Extraer ID y verificar formato |
| URL inválida | Mostrar error, solicitar URL válida |
| URL inválida (2da vez) | Ofrecer cambiar a Archivo |

---

## Paso 2: Extraer ID de tarea

- Parsear URL para obtener issue ID (formato: MCF-XXX)
- Validar formato con regex: `MCF-\d+`
- Si el formato es inválido → volver a Paso 1

---

## Paso 3: Obtener información de la tarea

- Usar herramienta `youtrack_get_issue` con el ID extraído
- Extraer: summary, description, estado actual

---

## Paso 4: Mostrar información

```
Issue MCF-XXX encontrado:

Título: ...
Descripción: ...
Estado: ...
```

**ACCIÓN REQUERIDA:** ESPERAR confirmación del usuario.

```
¿Deseas trabajar en esta tarea? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" / "sí" / "yes" | Continuar a Paso 5 |
| "no" | Volver a Paso 1 (solicitar otra URL) |
| Otra cosa | Solicitar "si" o "no" |

---

## Actualizar sesión después de confirmar tarea (YouTrack)

```markdown
### TASK_SOURCE
- [x] Solicitar fuente ("YouTrack")
- [x] Extraer ID de URL
- [x] Obtener información de tarea
- [x] Confirmar tarea

## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | ✅ | Completado |
| PLAN | 🔄 | Esperando tipo de rama |
```

---

## Continuar a Solicitar tipo de rama

---

# CONTINUACIÓN: Solicitar tipo de rama

**Este paso es común a ambos flujos después de obtener la tarea.**

**ACCIÓN REQUERIDA:** ESPERAR respuesta del usuario.

```
¿Cuál tipo de rama deseas crear?

1. feature    → Rama base: development
2. hotfix     → Rama base: main
```

| Respuesta | Rama base | Ejemplo |
|-----------|-----------|---------|
| "feature" / "1" | development | feature/MCF-XXX-descripcion |
| "hotfix" / "2" | main | hotfix/MCF-XXX-descripcion |

---

## Actualizar sesión después de confirmar tipo de rama

```markdown
### TASK_SOURCE
- [x] Solicitar fuente
- [x] Obtener tarea
- [x] Confirmar tarea
- [x] Solicitar tipo de rama

## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | ✅ | Completado |
| PLAN | 🔄 | Esperando iniciar |
```

---

## Continuar a Planificación

Una vez obtenido:
- Tarea (MCF-XXX)
- Tipo de rama
- Rama base

→ Leer `plan_workflow.md` y continuar.

---

## Resumen de Puntos de Espera

| Flujo | Paso | ¿Espera? | Input Esperado |
|-------|------|----------|----------------|
| Archivo | 1 | **SÍ** | Ruta de archivo |
| Archivo | 4 | **SÍ** | Número de tarea (1-N) |
| Archivo | 5 | **SÍ** | "si" / "no" |
| YouTrack | 1 | **SÍ** | URL de YouTrack |
| YouTrack | 4 | **SÍ** | "si" / "no" |
| Común | Rama | **SÍ** | "feature" / "hotfix" |
