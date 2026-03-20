# Workflow: Ejecución Paso a Paso

## Pasos

1. **Para cada paso del plan:**
   - Mostrar descripción y código
   - Esperar "next" del usuario
   - Ejecutar SOLO después de confirmación
   - Verificar: `make check`

2. **Verificación final**
   - Ejecutar `make check`
   - Mostrar resultados (lint, typecheck, tests)
   - Solo continuar si todo pasa
