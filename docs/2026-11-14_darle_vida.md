# Bitácora de Desarrollo: ProyectoKira

> **Estado del proyecto:** `En Desarrollo Activo` | **Modelo Base:** `qwen2.5:3b` y `qwen2.5vl:3b` (Ollama)

## Logros Técnicos Completados

| Módulo / Componente | Archivo | Implementación y Función |
| :--- | :--- | :--- |
| **Motor de Visión en RAM** | `src/vision_engine.py` | Captura proactiva del monitor principal mediante `mss` y procesamiento en memoria RAM (`io.BytesIO` con `Pillow`) sin dejar archivos temporales en disco. |
| **Escudo de Privacidad** | `src/privated_engine.py` | Aduana *Deny by Default* con `pygetwindow` que revisa todas las ventanas abiertas en ambos monitores y bloquea capturas ante palabras sensibles (`.env`, correos, bancos, contraseñas), enviando la señal `"BLOQUEADO"`. |
| **Memoria a Corto Plazo** | `src/memory_manager.py` | Ventana deslizante en RAM (`collections.deque`) que conserva el hilo reciente de conversación e incluye contexto visual sin almacenar bytes pesados. |
| **Cerebro Híbrido y Contexto** | `src/ollama_client.py` | Enrutamiento dinámico entre `qwen2.5:3b` (texto rápido) y `qwen2.5vl:3b` (visión), inyección del título real de ventana activa, control de personalidad *tsundere* en español neutro y ajuste de penalizaciones (`repeat_penalty`, `presence_penalty`, `frequency_penalty`). |
| **Detección Natural en Chat** | `src/cogs/chat.py` | Activación de visión por intención natural sin comandos rígidos, desempaquetado de captura + ventana activa e indicador de escritura en vivo. |

---

## Decisiones de Arquitectura y Alcance Descartado

* **Descarte temporal de síntesis y reconocimiento de voz (`src/cogs/voice.py`):** Se decidió pausar y descartar para esta etapa la integración de voz en canales de Discord (`ffmpeg`, `PyNaCl` / TTS) debido a que añadía fricción técnica innecesaria al MVP. Se priorizó consolidar primero los sentidos visuales, la privacidad estricta y la memoria conversacional.

---

## Próximos Pasos

* **Memoria Persistente (`SQLite`):** Crear `data/kira_memory.db` para almacenar hechos permanentes sobre el creador, el proyecto y preferencias que sobrevivan al reinicio del sistema.
* **Proactividad Autónoma (`tasks.loop`):** Implementar observación periódica en segundo plano protegida por el escudo de privacidad.

## Actualizaciones Futuras del Proyecto

- [ ] **Desarrollar una compañera a kira para complementar** se usarian las bases de kira para su desarrollo con cambios notables en cuanto objetivo y funciones añadidas que kira no tendra.
- [ ] **Base de datos y archivo JSON** Memoria de largo plazo escalable para retencion de conversaciones anteriores independientemente de la fecha y hora de la conversacion.
- [X] **Funcion observable** Capacidad de analizar la pantalla mediante cambios en la pantalla y toma de fotos temporales que se guardan en la RAM y se borran despues.
- [ ] **Cola de espera** Cola de espera dinamica, su funcion es evitar que kira y nova usen el modelo de ollama al mismo tiempo y no utilizen CPU Y GPU inecesario.

