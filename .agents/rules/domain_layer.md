# Domain Layer Rules
- Definir entidades de negocio en `src/domain/entities.py`.
- Definir interfaces (Ports) en `src/domain/interfaces.py` para desacoplar la lógica de la infraestructura.
- Implementar una jerarquía completa de excepciones de dominio en `src/domain/exceptions.py`.
- Las dependencias deben apuntar siempre hacia adentro (DIP).
