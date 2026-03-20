# Workflow: Planificación

## Regla Principal

**NO ejecutar ningún paso hasta haber leído completamente este workflow y tener la confirmación del usuario.**

---

## Pasos

### Paso 1: Extraer contexto

**ACCIÓN REQUERIDA:** Leer los siguientes archivos en orden:

| Archivo | Propósito |
|---------|-----------|
| `tasks.md` | Leer la tarea seleccionada completa |
| `design.md` | Arquitectura del sistema |
| `requirements.md` | Criterios de aceptación |

**NO CONTINUAR hasta haber leído los tres archivos.**

---

### Paso 2: Identificar skill aplicable

**ACCIÓN REQUERIDA:** Basado en la tarea, identificar skill correspondiente.

| Skill | Cuando usar |
|-------|-------------|
| `builders.md` | Tarea involucra Builders |
| `cache.md` | Tarea involucra ChromaCacheRepository |
| `class_format.md` | Cualquier tarea (formato de clases) |
| `controllers.md` | Tarea involucra Controllers FastAPI |
| `domain_layer.md` | Tarea involucra Entidades, Interfaces, Excepciones |
| `factories.md` | Tarea involucra Factory Pattern |
| `llm.md` | Tarea involucra LLM/Gemini |
| `providers.md` | Tarea involucra Proveedores |

**Leer el archivo de skill identificado y mostrar convenciones.**

---

### Paso 3: Crear plan de implementación

Basado en:
- Descripción de la tarea
- Convenciones del skill
- Criterios de requirements.md

Dividir en pasos ejecutables:
- Archivo(s) a crear
- Archivo(s) a modificar
- Test(s) a escribir

---

### Paso 4: Mostrar plan completo

**Usar `.agents/templates/plan_template.md` como referencia.**

Formato:
```
=================================================================
PLAN DE IMPLEMENTACIÓN
=================================================================
Tarea: MCF-XXX
Rama: feature/MCF-XXX-descripcion / hotfix/MCF-XXX-descripcion
Skill: nombre-del-skill.md

PASOS:
-------
[1] Crear archivo X
    - Descripción del paso
    - Archivos: src/...

[2] Implementar funcionalidad Y
    - Descripción del paso
    - Archivos: src/...

[3] Escribir tests
    - Descripción del paso
    - Archivos: tests/...

=================================================================
```

---

### Paso 5: Solicitar confirmación antes de crear rama

**ACCIÓN REQUERIDA:** ESPERAR respuesta del usuario.

```
¿Creamos la rama feature/MCF-XXX-descripcion? (si/no)
```

| Respuesta | Acción |
|-----------|--------|
| "si" / "sí" / "yes" | Crear rama desde base correspondiente |
| "no" | NO crear rama, preguntar qué hacer |
| Otra cosa | Solicitar "si" o "no" |

---

### Paso 6: Crear rama (si confirmado)

```bash
# Para feature
git checkout -b feature/MCF-XXX-descripcion development

# Para hotfix
git checkout -b hotfix/MCF-XXX-descripcion main
```

---

### Paso 7: Actualizar estado YouTrack

**SOLO ejecutar después de confirmación explícita.**

- Usar herramienta `youtrack_update_issue`
- Cambiar estado a "En curso" / "In Progress"

**ACCIÓN REQUERIDA:** ESPERAR confirmación.

```
¿Actualizamos el estado de la tarea a "En curso"? (si/no)
```

---

### Paso 8: Mostrar mensaje de espera

**ACCIÓN REQUERIDA:** Mostrar y ESPERAR "next".

```
=================================================================
Plan listo. Responder 'next' para iniciar la ejecución.
=================================================================

El workflow de ejecución (execute_workflow.md) ejecutará
cada paso esperando confirmación antes de continuar.
```

| Respuesta | Acción |
|-----------|--------|
| "next" | Leer `execute_workflow.md` e iniciar ejecución |
| "stop" | Detener, volver al estado anterior |
| Otra cosa | Mostrar que debe responder "next" o "stop" |

---

## Validaciones Antes de Continuar

| Validación | Requerimiento |
|------------|---------------|
| Rama base existe | `git branch -a` muestra development o main |
| Tarea en YouTrack creada | MCF-XXX accesible |
| make check disponible | `make --help` o `make lint` funciona |
| Skill identificado | Archivo existe en `skills/` |

---

## Estados de Espera

| Paso | ¿Espera? | Qué espera |
|------|----------|------------|
| 1 | No | Solo lectura |
| 2 | No | Solo lectura |
| 3 | No | Generación de plan |
| 4 | No | Mostrar plan |
| 5 | **SÍ** | "si" / "no" para crear rama |
| 6 | No | Solo ejecutar si paso 5 confirmado |
| 7 | **SÍ** | "si" / "no" para actualizar YouTrack |
| 8 | **SÍ** | "next" / "stop" |

---

## Continuar

Después de recibir "next" en Paso 8:
→ Leer `execute_workflow.md` e iniciar ejecución paso a paso.
