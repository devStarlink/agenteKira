# Bitácora de Desarrollo: ProyectoKira (15 de Noviembre, 2026)

> **Estado del proyecto:** `Versión 1.0 Lista para Publicación` | **Modelo Base:** `qwen2.5vl:3b` (Ollama) | **Persistencia:** `SQLite` (`data/kira_memory.db`)

---

## Resumen de la Sesión

Durante esta jornada se consolidó la arquitectura portable y persistente de **agenteKira**, eliminando configuraciones rígidas en código fuente, resolviendo bucles de eco en la memoria conversacional e incorporando aprendizaje atómico en dos niveles y visión multi-monitor nativa en memoria RAM.

---

## Logros Técnicos Completados

| Módulo / Componente | Archivo | Implementación y Función |
| :--- | :--- | :--- |
| **Base de Datos Persistente** | `src/database.py` | Creación automática de `data/kira_memory.db` mediante `sqlite3` y `pathlib`. Implementación de las tablas `configuracion` (clave/valor para personalidad) y `hechos` (memoria permanente con restricción `UNIQUE` para evitar duplicados). |
| **Asistente de Primer Arranque** | `src/setup_wizard.py` | Onboarding interactivo por consola que verifica credenciales (`.env`), solicita la personalidad del agente y ejecuta una entrevista de identidad inicial (apodo del usuario, propósito obligatorio y capacidades base) en instalaciones nuevas. |
| **Desacoplamiento y Estabilidad** | `src/ollama_client.py` | Lectura dinámica de personalidad y recuerdos desde `SQLite`. Ajuste de ventana de contexto (`num_ctx: 4096`), límite de salida (`num_predict: 250`) y aislamiento de respuestas visuales respecto a la RAM conversacional (`deque`) para eliminar bucles de eco. |
| **Memoria Híbrida (2 Niveles)** | `src/cogs/chat.py` y `src/ollama_client.py` | **Nivel 1 (Explícito):** Detección de intención natural (`"recuerda que..."`, `"recordar que..."`, `"anota que..."`) para almacenar datos permanentes en tiempo real.<br>**Nivel 2 (Silencioso):** Extractor asíncrono en segundo plano (`asyncio.create_task(extract_fact(...))`) con `temperature: 0.1` que comprime hechos relevantes en oraciones atómicas sin bloquear el chat. |
| **Visión Multi-Monitor en RAM** | `src/vision_engine.py` | Captura simultánea de todos los monitores conectados (`sct.monitors[1:]`) procesados en memoria RAM (`BytesIO` a `960x540` JPEG) y enviados en lote a `qwen2.5vl:3b`, manteniendo activo el escudo de privacidad *Deny by Default*. |
| **Documentación y Seguridad** | `.gitignore`, `README.md`, `requirements.txt` | Exclusión total de `.env`, `data/`, `venv/` y `__pycache__/`. Generación de dependencias congeladas y portada técnica del proyecto para despliegue en GitHub. |
| **Blindaje de Memoria y Personalidad** | `src/ollama_client.py` | Ajuste del extractor asíncrono (`extract_fact`) a `temperature: 0.0` y `num_predict: 40` con reglas estrictas de filtrado (captura de datos técnicos/biográficos permanentes y descarte absoluto de ruido o pruebas). Definición de *system prompt* imperativo y minimalista para evitar alucinaciones, autorreferencias y muletillas de IA en `qwen2.5vl:3b`. |
---

## Decisiones de Arquitectura Futuras y Descartes

* **Aislamiento de memoria visual vs. conversacional:** Se determinó no almacenar descripciones de capturas de pantalla dentro del buffer circular en RAM (`memory_manager.py`), evitando que el modelo ligero (`3B`) entre en bucles de repetición al alternar entre visión y chat casual.
* **Compresión de hechos atómicos:** En lugar de almacenar historiales de chat completos en `SQLite`, se optó por guardar únicamente hechos breves en tercera persona (`"El usuario..."`) bajo instrucción pasiva en el `system_prompt`, evitando saturación de contexto y menciones forzadas.
* **Control estricto del extractor:** Para evitar la contaminación de la tabla `hechos` con acciones pasajeras o pruebas de código, se eliminó la creatividad del extractor (`temperature: 0.0`) mediante ejemplos explícitos de exclusión, garantizando que solo se almacenen datos estructurales o técnicos definitivos.