---
description: Workflow de inicialización
---

# Workflow: Inicialización

## Regla Principal

**Este workflow inicia o retoma una sesión de trabajo. NO continúa automáticamente.**
**El archivo de sesión se crea/actualiza en `.context/session_YYYYMMDD_HHMMSS.md`**

---

## Paso 1: Buscar sesión activa

```bash
ls -la .context/session_*.md 2>/dev/null | tail -1
```

### Si existe sesión activa

Mostrar resumen:
```
================================================================
📋 SESIÓN ACTIVA ENCONTRADA
================================================================
Archivo: .context/session_YYYYMMDD_HHMMSS.md

Tarea: {TAREA}
Fecha: {FECHA}
Rama: {RAMA}

Flujo actual: {FLUJO}
Estado: {ESTADO}

================================================================
¿Qué deseas hacer?

1. retomar → Continuar desde donde quedó
2. nueva → Descartar sesión anterior e iniciar nueva
================================================================
```

**Esperar respuesta: "retomar" o "nueva"**

| Respuesta | Acción |
|-----------|--------|
| "retomar" | Leer session_*.md, retomar flujo |
| "nueva" | `rm .context/session_*.md`, continuar a paso 2 |

### Si NO existe sesión activa

Continuar a paso 2.

---

## Paso 2: Solicitar fuente de tareas

**ACCIÓN REQUERIDA:** Mostrar pregunta y ESPERAR respuesta.

```
¿De qué fuente quieres tomar las tareas?

1. Archivo local   → Proporciona la ruta del archivo .md con tareas
2. YouTrack      → Proporciona la URL del issue
```

**NO CONTINUAR hasta recibir respuesta.**

---

## Paso 3: Crear archivo de sesión

Después de confirmar la tarea:

```bash
# Generar nombre con fecha y hora actual
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_FILE=".context/session_${TIMESTAMP}.md"
```

Copiar plantilla:
```bash
cp .agents/templates/session-template.md "$SESSION_FILE"
```

Actualizar sesión:
```markdown
# Sesión: {TAREA}
Fecha: {FECHA}
Hora: {HORA}
Rama: {RAMA}

## Flujos

| Flujo | Estado |
|-------|--------|
| INIT | 🔄 |
| TASK_SOURCE | ⏳ |
| PLAN | ⏳ |
| EXECUTE | ⏳ |
| FINALIZE | ⏳ |
```

---

## Paso 4: Marcar INIT completado y continuar

Después de mostrar rol, skills, workflows y solicitar fuente:

**Actualizar sesión:**
```markdown
## Flujos

| Flujo | Estado | Paso Actual |
|-------|--------|-------------|
| INIT | ✅ | Completado |
| TASK_SOURCE | 🔄 | Esperando fuente |
| PLAN | ⏳ | No iniciado |
| EXECUTE | ⏳ | No iniciado |
| FINALIZE | ⏳ | No iniciado |
```

**Continuar a:** `task_source_workflow.md`

---

## Estados de Espera

| Paso | ¿Espera? | Qué espera |
|------|----------|------------|
| Buscar sesión | **SÍ** | "retomar" o "nueva" |
| Solicitar fuente | **SÍ** | "Archivo" / "YouTrack" / número |
