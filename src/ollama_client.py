import asyncio
import mss


from PIL import Image
from ollama import AsyncClient

from src.memory_manager import save_messages, get_history
from src.database import get_config, get_all_facts, save_fact

async def consult(prompt: str, modelo: str = "qwen2.5vl:3b", imagen: bytes | str | None = None, ventana: str | None = None, save_to_history: bool = True, system_event: str | None = None) -> str:
   try:
        personalidad = get_config("personalidad") or "Eres Kira, una asistente directa."

        hechos = get_all_facts()
        texto_hechos = "\n- ".join(hechos) if hechos else "Ninguno aún."
        system_prompt = f"{personalidad}\n\n[DATOS DE REFERENCIA SILENCIOSOS - PROHIBIDO MENCIONARLOS SI EL USUARIO NO PREGUNTA POR ELLOS]:\n{texto_hechos}"

        if system_event:
            system_prompt +=  f"\n\n[EVENTO INTERNO ACTUAL]: {system_event}"
        system_prompt += "\n\nRegla estricta: Da una sola respuesta directa y detente de inmediato. Nunca simules turnos de conversación ni repitas saludos."

        message_user = {
            'role': 'user',
            'content': prompt,
        }

        memories = get_history()

        if imagen == "BLOQUEADO":
            modelo = "qwen2.5vl:3b"
            historial = [
                {
                    'role': 'system',
                    'content': f"{system_prompt} no puedes ver la pantalla porque el usuario tiene algo privado abierto, pidele que lo cierre segun tu personalidad.",
                },
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]

        elif imagen is not None:
            modelo = "qwen2.5vl:3b"
            historial = [
                {
                        'role': 'system',
                        'content': (
                                        f"{system_prompt}\n\n"
                                        "Estás viendo las capturas de los monitores del usuario (Imagen 1 es el monitor izquierdo, Imagen 2 es el monitor derecho). "
                                        "Ignora la ventana de Discord donde chatean y responde directamente qué aplicación, archivo o código ves en el otro monitor, "
                                        "conectándolo con lo que acaban de hablar en máximo 2 oraciones directas."
                                   ),
        },
        *memories[-2:],
        {
            'role': 'user',
            'content': f"[Ventana activa: {ventana}]\n{prompt}",
            'images': [imagen],
        },
    ]
        else:
            historial = [
                {'role': 'system', 'content': system_prompt},
                *memories,
                message_user,
            ]

        answer = await AsyncClient().chat(
            model=modelo,
            messages=historial,
            options={
                "repeat_penalty": 1.3,
                "num_predict": 55 if system_event else 140,
                "temperature": 0.25 if isinstance(imagen, list) else 0.45,
                "num_ctx": 4096,
                "stop": ["Jefe:", "Usuario:", "User:", "\n\n\n"]
            }
        )

        reply = answer['message']['content']

        if system_event or len(prompt.strip()) < 25:
            reply = reply.split("\n")[0].strip()

        if imagen is None and save_to_history:
            save_messages('user', prompt)
            save_messages('assistant', reply)

        return reply
   
   except Exception as e:
        import traceback
        traceback.print_exc()
        return f"An error occurred while connecting to Ollama: {e}"