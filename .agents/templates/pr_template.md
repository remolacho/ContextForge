# Plantilla: Pull Request

## Título

```
{MCF-XXX}: {descripción breve de la tarea}
```

**Ejemplo:** `MCF-123: Implementar ContextItemBuilder`

---

## Body

### Summary

{puntos clave de la implementación}

**Ejemplo:**
- Implementar ContextItemBuilder con API fluida para construir ContextItem
- Implementar CacheEntryBuilder con API fluida para construir CacheEntry
- Agregar property tests para verificar hash SHA-256 determinista

---

### Changes

| Tipo | Archivos |
|------|----------|
| Creados | `src/infrastructure/builders/context_item.py` |
| Creados | `src/infrastructure/builders/cache_entry.py` |
| Creados | `tests/property/test_properties_builders.py` |

---

### Verification

| Verificación | Estado |
|--------------|--------|
| Lint (`make lint`) | ✅ passed |
| Typecheck (`make typecheck`) | ✅ passed |
| Tests (`make test`) | ✅ passed |

**Comando completo:**
```bash
make check
```

---

### Links

| Recurso | URL |
|---------|-----|
| YouTrack | https://communities.youtrack.cloud/issue/{MCF-XXX} |
| Sprint | https://communities.youtrack.cloud/agiles/195-1/current |

---

## Metadatos (auto-llenados por gh)

- **Base:** development (feature) / main (hotfix)
- **Head:** feature/{MCF-XXX}-descripcion
- **Commits:** 1 (squash)

---

## Checklist Pre-PR

- [ ] make check pasa localmente
- [ ] Tests nuevos incluidos
- [ ] ID de YouTrack en título
- [ ] Descripción clara de cambios
- [ ] Commits squashed a 1
