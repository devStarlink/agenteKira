# Documentación Técnica: Sistema de Proactividad y Gestión de Memoria



Este documento detalla las nuevas funcionalidades implementadas en el bot, enfocándose en el monitoreo de eventos del sistema, la proactividad automatizada, la optimización del cliente de Ollama y el gestor de memoria a corto plazo.



## 1. Arquitectura General de las Novedades



El sistema ha evolucionado de un modelo puramente reactivo a uno **proactivo**, capaz de detectar acciones del usuario en su entorno local (Windows) e iniciar interacciones naturales a través de Discord sin intervención manual.



### Componentes Nuevos y Actualizados



1. **`src/proactivity/system_events.py`**: Monitor de procesos del sistema operativo.

2. **`src/proactivity/proactivity.py`** *(Cog)*: Tarea en segundo plano que conecta los eventos del sistema con el LLM y Discord.

3. **`src/ollama_client.py`**: Actualizado para soportar eventos internos (`system_event`), control de historial selectivo y ajustes dinámicos de parámetros de inferencia.

4. **`src/memory_manager.py`**: Gestor de historial conversacional acotado en memoria RAM.

5. **`requirements.txt`**: Incorporación de `psutil` para la inspección de procesos.



---



## 2. Módulo de Eventos del Sistema (`system_events.py`)



La clase `SystemEventsManager` se encarga de vigilar la ejecución de aplicaciones específicas en el equipo local utilizando la librería `psutil`.



### Funcionamiento



* **Lista de Vigilancia (`watched_apps`)**: Mapea nombres de ejecutables a nombres amigables:

  * `code.exe` -> *Visual Studio Code*

  * `steam.exe` -> *Steam*

  * `spotify.exe` -> *Spotify*

* **Detección de Apertura**: En cada verificación, compara los procesos activos actuales contra un conjunto de procesos conocidos previamente (`self.known_processes`). Si un ejecutable vigilado aparece y no estaba en la lista anterior, se dispara la detección.

* **Control de Frecuencia (*Cooldown*)**: Implementa un temporizador (`cooldown`, por defecto `3600` segundos / 1 hora) para evitar que el bot envíe mensajes repetitivos si el usuario abre y cierra aplicaciones constantemente.



---



## 3. Cog de Proactividad (`proactivity.py`)



`ProActivityCog` integra el monitor de eventos dentro del ciclo de vida de `discord.py`.



### Flujo de Ejecución



1. **Bucle de Monitoreo (`@tasks.loop(seconds=10)`)**: Se ejecuta cada 10 segundos una vez que el bot está listo (`before_system_monitor`).

2. **Validación de Canal**: Verifica que exista un canal activo registrado en `self.bot.ultimo_canal`.

3. **Generación de Respuesta Contextual**: Si `check_events()` devuelve una aplicación recién abierta, el bot simula estar escribiendo (`typing()`) y consulta a Ollama pasando un `system_event` oculto para que el modelo genere un comentario casual de una sola oración sin ofrecer asistencia técnica.

4. **Aislamiento de Memoria**: Envía `save_to_history=False` para que estos comentarios espontáneos no contaminen el contexto de las conversaciones principales.



---



## 4. Actualizaciones en el Cliente de Ollama (`ollama_client.py`)



La función `consult()` ha sido refactorizada para manejar distintos contextos de interacción con el modelo `qwen2.5vl:3b`.



### Nuevos Parámetros



* `save_to_history: bool = True`: Permite decidir si la interacción actual debe guardarse en la memoria a corto plazo.

* `system_event: str | None = None`: Inyecta una directiva `[EVENTO INTERNO ACTUAL]` en el *System Prompt* para guiar el comportamiento del modelo ante disparadores automáticos.



### Optimizaciones de Inferencia



* **Límite de Tokens (`num_predict`)**: Se reduce dinámicamente a `55` tokens cuando se trata de un `system_event` (frente a `140` en chat normal) para garantizar respuestas breves y directas.

* **Temperatura Dinámica**: Se ajusta a `0.25` cuando se analizan múltiples imágenes (capturas de pantalla) para mayor precisión, y a `0.45` en interacciones de texto para mayor naturalidad.

* **Post-procesamiento de Respuesta**: Si la consulta proviene de un evento del sistema o es un prompt muy corto (< 25 caracteres), la respuesta se recorta al primer salto de línea (`split("\n")[0]`) para evitar alucinaciones o turnos simulados.

* **Soporte de Privacidad en Visión**: Manejo explícito del estado `imagen == "BLOQUEADO"`, instruyendo al modelo a pedir al usuario que cierre ventanas privadas según su personalidad configurada.



---



## 5. Gestor de Memoria a Corto Plazo (`memory_manager.py`)



Implementa un búfer circular ligero utilizando `collections.deque`.



* **Capacidad (`maxlen=4`)**: Mantiene únicamente los últimos 4 mensajes (2 turnos completos de usuario-asistente) para mantener la ventana de contexto (`num_ctx: 4096`) rápida y relevante.

* **Truncado Automático**: Cada mensaje guardado se recorta a un máximo de `300` caracteres (`save_messages`) para evitar el desbordamiento de tokens por textos largos.

* **Funciones Expuestas**: `save_messages()`, `get_history()` y `clear_memory()`.



---



## 6. Dependencias Añadidas (`requirements.txt`)



Para habilitar estas características, se actualizó el entorno con las siguientes librerías clave:



* `psutil==7.2.2`: Lectura e iteración de procesos del sistema operativo.

* `mss==10.2.0` & `pillow==13.0.0`: Captura y procesamiento de múltiples monitores para el modo visión.

* `PyGetWindow==0.0.9`: Obtención del título de la ventana activa (`[Ventana activa: ...]`).

* `ollama==0.6.3` & `discord.py==2.7.1`: Comunicación asíncrona con el LLM local y la API de Discord.