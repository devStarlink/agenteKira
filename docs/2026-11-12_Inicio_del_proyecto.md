# Bitacora de Inicio - Proyecto KiraStudio / AsistentKira
**Fecha: ** 2026-11-12
**Estado: ** Fase de diseño y estructura modular.

## Objetivos
* Desarrollar un asistente de escritorio local con enfoque en privacidad ("Deny by Default").
* Aislar la lógica en módulos independientes (`bot_core.py`, `privacy_shield.py`, etc.).
* Mantener un control estricto de credenciales mediante variables de entorno (`.env`).

<details>
<summary>Notas de Arquitectura</summary>
* Se optó por una estructura modular en lugar de un script monolítico para facilitar el mantenimiento y evitar fallos cruzados entre el bot de Discord y el escudo de privacidad sobre todo en futuras actualizaciones.
</details>

## Avances del día (12 de noviembre de 2026)

### 1. Corrección de núcleo y arranque (`src/bot_core.py`)
- Se corrigió un error tipográfico en el constructor de la clase `KiraBot` (`__int__` -> `__init__`) que impedía inicializar correctamente `command_prefix` y los permisos de `intents`[cite: 1, 2, 3].
- Se verificó el funcionamiento del filtro de seguridad **"Deny by Default"** mediante `owner_id`, logrando la primera conexión exitosa y respuesta básica en el servidor de Discord[cite: 3, 5].

### 2. Arquitectura Modular (Cogs)
- Se implementó el método `setup_hook` en `KiraBot` para la carga dinámica y automática de extensiones desde `src/cogs/`.
- Se creó la carpeta `src/cogs/` para aislar funcionalidades por módulos independientes[cite: 6].

### 3. Integración de Voz (`src/cogs/voice.py`)
- Se instalaron las dependencias de audio y cifrado necesarias (`discord.py[voice]` / `PyNaCl` / `davey`) dentro del entorno virtual (`venv`)[cite: 6].
- Se desarrolló el módulo `VoiceCog` con los comandos:
  - `!entrar`: Conecta a Kira al canal de voz activo del usuario o la mueve si ya está en otro canal[cite: 6, 7].
  - `!salir`: Desconecta a Kira del canal de voz de forma manual[cite: 6].
- Se probó con éxito la conexión al canal de voz en Discord[cite: 7].y