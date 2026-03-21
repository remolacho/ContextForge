# Plantilla: Pull Request

## Uso

Esta plantilla se usa dinámicamente en el workflow de finalización.
El agente genera el contenido basándose en la sesión activa.

---

## Título

```
MCF-{ID}: {título de la tarea}
```

---

## Body (generado dinámicamente)

El agente genera:

```markdown
## Summary

- {cambio 1 realizado en EXECUTE}
- {cambio 2 realizado en EXECUTE}
- Tests agregados/verificados

## Changes

| Tipo | Archivos |
|------|----------|
| Creados | archivo1.py |
| Modificados | archivo2.py |

## Verification

| Verificación | Estado |
|--------------|--------|
| Lint (`make lint`) | ✅ passed |
| Typecheck (`make typecheck`) | ✅ passed |
| Tests (`make test`) | ✅ passed |

## Links

| Recurso | URL |
|---------|-----|
| YouTrack | https://communities.youtrack.cloud/issue/{MCF-XXX} |
| Sprint | https://communities.youtrack.cloud/agiles/195-1/current |
```

---

## Metadatos

- **Base:** development (feature) / main (hotfix)
- **Head:** feature/{MCF-XXX}-descripcion
- **Commits:** N → 1 (squash automático por GitHub)

---

## Verificación Pre-PR

- [ ] `make check` pasa localmente
- [ ] Commits en rama: N (serán squash a 1)
- [ ] ID de YouTrack en título
- [ ] Descripción refleja lo realizado en EXECUTE
