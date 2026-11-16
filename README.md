# agenteKira

Agente de inteligencia artificial local y reactivo integrado en Discord, impulsado por **Ollama** (`qwen2.5vl:3b`), con visión multi-monitor en memoria RAM, escudo de privacidad *Deny by Default*, memoria persistente en **SQLite** y asistente interactivo de primer arranque.

---

## Características Principales

* **100 % Local y Privado:** Ejecución completa en tu equipo mediante Ollama sin enviar datos ni capturas a APIs externas.
* **Visión Multi-Monitor en RAM (`BytesIO`):** Captura y analiza todas tus pantallas conectadas bajo demanda sin guardar archivos temporales en disco.
* **Escudo de Privacidad (*Deny by Default*):** Bloquea automáticamente la captura de pantalla si detecta ventanas sensibles (bancos, gestores de contraseñas, configuración o modo incógnito).
* **Memoria Híbrida Persistente (`SQLite`):**
  * **Corto plazo (`deque`):** Mantiene el hilo reciente de la conversación en RAM.
  * **Largo plazo (`data/kira_memory.db`):** Almacena la personalidad, identidad y hechos atómicos aprendidos tanto de forma explícita (*"Recuerda que..."*) como mediante extracción silenciosa en segundo plano.
* **Asistente de Primer Arranque (`setup_wizard.py`):** Configura automáticamente `.env` y la base de datos local la primera vez que se ejecuta el proyecto.

---

## Requisitos Previos

* **Sistema Operativo:** Windows 10 / 11 (utiliza `pygetwindow` para detección de ventanas activas).
* **Python:** `3.10` o superior.
* **Ollama:** Instalado y en ejecución con el modelo multimodal descargado:
  ```bash
  ollama pull qwen2.5vl:3b
  ```
* **Bot de Discord:** Token de aplicación con el *Privileged Gateway Intent* **Message Content Intent** activado.

* **Hardware Recomendado:**
  * **RAM:** Mínimo `8 GB` (`16 GB` recomendados para ejecutar Windows, Discord y Ollama con fluidez).
  * **GPU (Opcional pero recomendada):** Tarjeta gráfica con al menos `4 GB` de VRAM (NVIDIA/AMD) para respuestas rápidas; también funciona en CPU aunque con mayor tiempo de respuesta.
  * **Almacenamiento:** Alrededor de `3.5 GB` libres para descargar el modelo `qwen2.5vl:3b`.


---

## Instalación y Uso

1. **Clona el repositorio y crea tu entorno virtual:**
   ```bash
   git clone https://github.com
   cd agenteKira
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta el agente:**
   ```bash
   python main.py
   ```
   > En el primer arranque, el asistente interactivo en consola te solicitará tu `DISCORD_TOKEN`, tu `MY_USER_ID` (aislamiento estricto de propietario), la personalidad del agente y su identidad base.

---

## Arquitectura del Proyecto

```text
agenteKira/
├── data/                   # Base de datos SQLite local (excluida en .gitignore)
├── docs/                   # Bitácoras técnicas de desarrollo
├── src/
│   ├── cogs/
│   │   ├── chat.py         # Listener de Discord, disparadores de memoria y visión
│   │   └── voice.py        # Módulo base de voz (descartada pero aun con acceso a canales de voz)
│   ├── bot_core.py         # Núcleo del cliente de Discord y carga de extensiones
│   ├── database.py         # Gestión de SQLite (tablas configuracion y hechos)
│   ├── memory_manager.py   # Buffer circular en RAM para contexto inmediato
│   ├── ollama_client.py    # Integración con Ollama (chat, visión y extractor de hechos)
│   ├── privated_engine.py  # Filtro de privacidad Deny by Default
│   ├── setup_wizard.py     # Onboarding interactivo de instalación
│   └── vision_engine.py    # Captura de pantalla multi-monitor en RAM con mss y Pillow
├── main.py                 # Punto de entrada principal
└── requirements.txt        # Dependencias del proyecto
```

---

## Notas de Uso en Discord

* **Mensajes Directos (MD):** Puedes chatear con Kira tanto en canales de servidor como por Mensaje Directo privado (asegúrate de tener activada la opción *Permitir mensajes directos de miembros del servidor* en los ajustes de privacidad de tu servidor).
* **Uso Multi-Agente:** Si ejecutas **agenteKira** junto a otros bots propios en el mismo servidor (por ejemplo, *Nova*), asigna **canales de texto separados** para cada agente ajustando permisos de lectura por canal para evitar que respondan al mismo tiempo.
* **Aislamiento Estricto de Propietario (`MY_USER_ID`):** Por seguridad y privacidad (ya que el agente puede capturar tus pantallas), el bot **solo responde al usuario cuyo ID de Discord fue configurado** durante el asistente inicial. Si otra persona le escribe en el servidor o por MD, el bot ignorará el mensaje por completo.
