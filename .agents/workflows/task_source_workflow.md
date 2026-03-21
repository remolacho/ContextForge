# Workflow: Fuente de Tareas

## Regla Principal

**DOS flujos: ARCHIVO o YOUTRACK. Siempre igual.**

---

## FLUJO A: ARCHIVO LOCAL

### Paso 1: Solicitar ruta

```
Proporciona la ruta al archivo de tareas (.md):
Ejemplo: tasks.md o docs/tasks.md
```

**Esperar respuesta.**

---

### Paso 2: Verificar existencia

→ Leer `.agents/skills/workflow/validate_file_exists.md`

| Resultado | Acción |
|-----------|--------|
| Existe | Continuar a Paso 3 |
| No existe | Mostrar error, volver a Paso 1 |

---

### Paso 3: Leer archivo

- Leer archivo completo
- Extraer tareas con formato `- [ ]`
- Mostrar lista

---

### Paso 4: Listar tareas

```
Tareas disponibles:

[1] Título tarea 1
[2] Título tarea 2
[3] Título tarea 3
...

Puedes seleccionar varias usando comas: 1,3
o un rango: 1-3
o 'todas' para seleccionar todas
```

**Esperar respuesta (números, rango, o "todas").**

---

### Paso 5: Confirmar tareas seleccionadas

Mostrar tareas seleccionadas:
```
Tareas seleccionadas (3):
1. Título tarea 1
2. Título tarea 2
3. Título tarea 3
```

→ Leer `.agents/skills/workflow/wait_yes_no.md`

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a Paso 6 |
| "no" | Volver a Paso 4 |

---

### Paso 6: Crear UNA SOLA tarea en YouTrack ⚠️ OBLIGATORIO

**REGLA CRÍTICA: Se crea UNA SOLA tarea en YouTrack, sin importar cuántas se seleccionaron.**

→ Leer `.agents/skills/youtrack/create_issue.md`

Todas las tareas seleccionadas se combinan en UN SOLO issue:

**Título:** `{título de la primera tarea} (+N más)` si hay varias

**Descripción:**
```markdown
## Tareas del batch

### 1. Título tarea 1
Descripción de la tarea 1...

### 2. Título tarea 2
Descripción de la tarea 2...

### 3. Título tarea 3
Descripción de la tarea 3...
```

→ Ejecutar `youtrack_create_issue` UNA SOLA VEZ:

```
Creando tarea en YouTrack...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MCF-XXX: Título tarea 1 (+2 más)
→ https://communities.youtrack.cloud/issue/MCF-XXX ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 1 tarea creada con 3 subtareas combinadas
```

---

Continuar a Solicitar tipo de rama.

---

## FLUJO B: YOUTRACK URL

### Paso 1: Solicitar URL

```
Proporciona la URL del issue de YouTrack:
Ejemplo: https://communities.youtrack.cloud/issue/MCF-123
```

**Esperar respuesta.**

---

### Paso 2: Validar URL

Regex: `MCF-\d+`

| Resultado | Acción |
|-----------|--------|
| Válido | Continuar a Paso 3 |
| Inválido | Mostrar error, volver a Paso 1 |

---

### Paso 3: Obtener información

→ Leer `.agents/skills/youtrack/get_issue.md`

Extraer: summary, description, estado.

---

### Paso 4: Mostrar y confirmar

```
Issue MCF-XXX encontrado:

Título: ...
Descripción: ...
Estado: ...
```

→ Leer `.agents/skills/workflow/wait_yes_no.md`

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a Solicitar tipo de rama |
| "no" | Volver a Paso 1 |

---

Continuar a Solicitar tipo de rama.

---

## CONTINUACIÓN: Tipo de rama

```
¿Cuál tipo de rama deseas crear?

1. feature    → Rama base: development
2. hotfix     → Rama base: main
```

**Esperar respuesta.**

| Respuesta | Rama base |
|-----------|-----------|
| "feature" / "1" | development |
| "hotfix" / "2" | main |

---

## Validación TASK_SOURCE completado

Antes de continuar a PLAN, verificar:

| Check | Validar |
|-------|----------|
| Fuente | YouTrack URL o Archivo seleccionado |
| Tarea | Confirmada por usuario |
| YouTrack | Issue ID (MCF-XXX) obtenido |
| Rama tipo | feature o hotfix seleccionado |

**Si falta algo:**
```
❌ ERROR: TASK_SOURCE incompleto.

Verificar:
[ ] Fuente de tarea seleccionada
[ ] Tarea confirmada
[ ] YouTrack issue ID obtenido
[ ] Tipo de rama seleccionado
```

**Si todo completo:**
```
✅ TASK_SOURCE completado.
Continuando a PLAN...
```

→ Leer `.agents/skills/session/update.md`

Actualizar sesión:
```markdown
| 3. TASK_SOURCE | ✅ | Fuente: {fuente}, Rama: {tipo} |
| 4. Tipo_rama | ✅ | {feature/hotfix} |
```

---

Continuar a Planificación.
