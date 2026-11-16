# Bitácora de Desarrollo: Proyecto Kira

> **Estado del Proyecto:** `En Desarrollo Activo` | **Modelo Base:** `qwen2.5:3b` (Ollama) | **Voz:** `es-MX-DaliaNeural`

---

## 1. Logros Técnicos Completados

| Módulo / Componente | Archivo | Implementación y Función |
| :--- | :--- | :--- |
| **Cerebro Local** | `src/ollama_client.py` | Implementación asíncrona mediante `ollama.AsyncClient` con `qwen2.5:3b` para evitar bloquear el *event loop* de Discord. |
| **Arquitectura Modular** | `src/cogs/chat.py` | Carga dinámica del Cog de conversación en `bot_core.py`. Filtra mensajes con `self.bot.user` y `self.bot.owner_id`, ignorando comandos con prefijo `!`. |
| **Identidad de Kira** | *System Prompt* | Configuración de personalidad *tsundere* (sin groserías graves) usando *Few-Shot Prompting* e inyección interna para mantener coherencia en español. |
| **Síntesis de Voz (TTS)** | `src/tts_engine.py` | Integración de `edge-tts`, `PyNaCl` y `FFmpeg`. Genera audio neuronal (`es-MX-DaliaNeural`) directo en memoria RAM usando `io.BytesIO`. |

---

## 2. Obstáculos Resueltos y Aprendizajes

* **Control de flujo en modelos ligeros (`3b`):** Los modelos pequeños tienden a salirse de personaje o repetir ejemplos si no se refuerza la instrucción del sistema en el último turno del usuario.
* **Límites de transmisión de voz en Discord (`VoiceClient`):** A pesar de configurar `libopus`, `davey`, el permiso *Speak* y la generación de `.mp3`, el envío UDP/WebRTC hacia los nodos de voz de Discord sufre silenciamiento en entornos Windows/Sonar.

> **Decisión de Arquitectura (Pivote):** 
> Dado que **Kira** es un asistente personal de ejecución local, enviar audio ida y vuelta a través de servidores externos añade latencia innecesaria. Se decidió **reproducir el audio directamente en la salida local de Windows desde la memoria RAM**.

---

## 3. Siguientes Pasos (Próxima Sesión)

- [ ] **Audio en RAM sin archivos temporales:** Implementar la reproducción local directa con `pygame.mixer` para eliminar `temp_kira.mp3` y escuchar a Kira al instante en los audífonos.
- [ ] **Seguridad y limpieza del repositorio:** Asegurar que `*.mp3` esté listado en `.gitignore` y verificar la rotación del `DISCORD_TOKEN`.


## Actualizaciones Futuras del Proyecto

- [ ] **Desarrollar una compañera a kira para complementar** se usarian las bases de kira para su desarrollo con cambios notables en cuanto objetivo y funciones añadidas que kira no tendra.
- [ ] **Base de datos y archivo JSON** Memoria de largo plazo escalable para retencion de conversaciones anteriores independientemente de la fecha y hora de la conversacion.
- [ ] **Funcion observable** Capacidad de analizar la pantalla mediante cambios en la pantalla y toma de fotos temporales que se guardan en la RAM y se borran despues.
- [ ] **Cola de espera** Cola de espera dinamica, su funcion es evitar que kira y nova usen el modelo de ollama al mismo tiempo y no utilizen CPU Y GPU inecesario.