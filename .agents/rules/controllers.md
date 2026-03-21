# Controllers Rules
- Utilizar el patrón FastAPI con controladores basados en clases.
- Heredar de `ApplicationController`.
- Los controladores deben ser delgados (thin), delegando la lógica de negocio a los correspondientes Handlers (Strategy Pattern).
- Gestionar la serialización de respuestas mediante schemas Pydantic.
- Los Handlers se ubican en `app/handlers/` (antes `app/services/handlers/`).
