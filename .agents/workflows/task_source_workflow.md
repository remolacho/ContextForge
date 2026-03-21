# Workflow: Fuente de Tareas

## Regla Principal

**DOS flujos: ARCHIVO o YOUTRACK. Siempre igual.**

---

## FLUJO A: ARCHIVO LOCAL

### Paso 1: Solicitar ruta

```
Proporciona la ruta al archivo de tareas (.md):
Ejemplo: .kiro/specs/contextforge/tasks.md
```

**Esperar respuesta.**

---

### Paso 2: Verificar existencia

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
...

¿Cuál tarea deseas tomar?
```

**Esperar número (1-N).**

---

### Paso 5: Confirmar tarea

Mostrar tarea seleccionada.

**Esperar "si" o "no".**

| Respuesta | Acción |
|-----------|--------|
| "si" | Continuar a Paso 6 |
| "no" | Volver a Paso 4 |

---

### Paso 6: Crear tarea en YouTrack ⚠️ OBLIGATORIO

**NO SKIP. Este paso es obligatorio.**

- Usar `youtrack_create_issue`
- Project: ContextForge
- Sprint: https://communities.youtrack.cloud/agiles/195-1/current
- Crear UNA tarea con título y descripción completos

Mostrar resultado:
```
Tarea creada en YouTrack:
https://communities.youtrack.cloud/issue/MCF-XXX
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

Usar `youtrack_get_issue` con el ID.

Extraer: summary, description, estado.

---

### Paso 4: Mostrar y confirmar

```
Issue MCF-XXX encontrado:

Título: ...
Descripción: ...
Estado: ...
```

**Esperar "si" o "no".**

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

Continuar a Planificación.
