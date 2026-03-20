# ContextForge

**ContextForge** es un servidor especializado de **Model Context Protocol (MCP)** desarrollado en Python y dockerizado, diseñado para optimizar el consumo de tokens proporcionando contexto preciso y eficiente a agentes de Inteligencia Artificial.

## 🚀 Propósito
El objetivo principal de ContextForge es actuar como un intermediario inteligente entre los agentes de IA (como Cursor) y diversas fuentes de datos (YouTrack, Jira, Git, etc.), permitiendo que el agente solicite exactamente el nivel de detalle que necesita mediante el uso de caché persistente y procesamiento avanzado de lenguaje natural.

## 🛠️ Herramientas Principales
El servidor expone tres capacidades fundamentales para la gestión de contexto:
- **Lectura Completa (`read_full`):** Recupera la totalidad del contenido de un ítem.
- **Resumen Inteligente (`read_summarize`):** Genera una versión condensada del contexto utilizando LLM para reducir el uso de tokens.
- **Fragmentación Estratégica (`read_chunks`):** Divide el contenido en fragmentos manejables, permitiendo el acceso a secciones específicas.

## 🏗️ Arquitectura y Diseño
El proyecto está construido bajo los principios de **Clean Architecture** y **SOLID**, garantizando un sistema modular y escalable:
- **Independencia de Proveedores:** Soporte extensible para múltiples fuentes de datos.
- **Capa de Dominio Pura:** Lógica de negocio aislada de la infraestructura.
- **Patrones de Diseño:** Implementación de Factory, Facade, Builder y Repository para una gestión robusta de componentes.

## 💻 Tecnologías Utilizadas
ContextForge utiliza una pila tecnológica moderna y eficiente:
- **Lenguaje:** Python 3.11+
- **Framework Web:** FastAPI (Interfaz MCP sobre HTTP)
- **IA & LLM:** Google Gemini a través de LangChain y LangGraph.
- **Caché Vectorial:** ChromaDB para almacenamiento persistente de contexto.
- **Tokenización:** Tiktoken para el conteo preciso de tokens.
- **Gestión de Configuración:** Pydantic y Pydantic-Settings.
- **Entorno de Ejecución:** Docker y Docker Compose.
- **Calidad de Código:** Pytest y Hypothesis para pruebas unitarias y de propiedades.

## 📦 Despliegue
El sistema está diseñado para ejecutarse de forma aislada mediante contenedores Docker, facilitando su integración con clientes que soporten el protocolo MCP.
