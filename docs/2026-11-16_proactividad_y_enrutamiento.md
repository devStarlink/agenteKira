# Bitácora de Desarrollo: ProyectoKira (16 de Noviembre, 2026)

> **Estado del proyecto:** `Rama experimental (Proactividad v0.1)` | **Modelo Base:** `qwen2.5vl:3b` (Ollama) | **Persistencia:** `SQLite` (`data/kira_memory.db`)

---

## Resumen de la Sesión

Durante esta jornada se consolidó el enrutamiento determinista basado en expresiones regulares para erradicar falsos positivos de visión y memoria, se aisló el entorno de desarrollo mediante ramas de Git (`experimental`) y se implementó el primer módulo funcional de iniciativa propia (**proactividad por inactividad**) desacoplado de la base de datos.

---

## Logros Técnicos Completados

| Módulo / Componente | Archivo | Implementación y Función |
| :--- | :--- | :--- |
| **Enrutamiento Determinista** | `src/extract_manager.py` y `src/cogs/chat.py` | Migración de tuplas simples (`in`) a patrones compilados (`re.compile` con límites `\b`) para activar tanto la captura de pantalla como el filtro de memoria Nivel 1, eliminando disparos accidentales y contaminación de contexto. |
| **Desacoplamiento de Extracción** | `src/extract_manager.py` | Separación de la lógica de extracción de hechos fuera del flujo principal de conversación para liberar la ventana de atención de `qwen2.5vl:3b` y mantener la estabilidad del personaje. |
| **Entorno Experimental en Git** | Rama `experimental` | Creación de rama aislada respecto a `main` para desarrollar e integrar nuevas capacidades sin comprometer la versión estable publicada en GitHub. |
| **Gestor de Inactividad** | `src/proactivity/inactivity_manager.py` | Implementación de la clase `InactivityManager` en Python puro para gestionar el cronómetro de silencio (`downtime`), tiempo de enfriamiento anti-spam (`cooldown`) y registro de interacciones del propietario. |
| **Cog de Proactividad** | `src/cogs/proactivity.py` y `src/bot_core.py` | Creación de `ProActivityCog` con bucle asíncrono (`@tasks.loop`) que monitorea `self.bot.ultimo_canal` y dispara saludos breves mediante `consult()` usando selección aleatoria de enfoques (`random.choice`) y contexto horario. |

---

## Decisiones de Arquitectura y Descartes

* **Lógica temporal y de eventos en Python, no en el LLM:** Se determinó que el cálculo de tiempos de silencio, *cooldowns* y futuras detecciones de sistema recaigan exclusivamente en Python, enviando a `qwen2.5vl:3b` únicamente una instrucción corta de generación para evitar sobrecarga cognitiva y alucinaciones.
* **Aislamiento de la base de datos en mensajes proactivos:** `ProActivityCog` consulta directamente a `ollama_client.py` sin invocar `extract_manager.py`, garantizando que los *prompts* internos de iniciativa propia jamás se almacenen ni contaminen la tabla `hechos` en `SQLite`.
* **Descarte de visión automática en inactividad:** Se optó por no adjuntar capturas de pantalla automáticas cuando el agente inicia conversación por silencio, evitando consumo innecesario de VRAM y manteniendo respuestas breves mediante rotación de intenciones textuales.
* **Modularización de proactividad:** Se separó la lógica de inactividad temporal (`inactivity_manager.py`) de la futura detección de eventos del sistema operativo (`system_events.py`) bajo el paquete `src/proactivity/` para facilitar pruebas unitarias y mantenimiento.
