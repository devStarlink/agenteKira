import asyncio
import mss


from PIL import Image
from ollama import AsyncClient

from src.memory_manager import save_messages, get_history
from src.database import get_config, get_all_facts, save_fact

async def consult(prompt: str, modelo: str = "qwen2.5vl:3b", imagen: bytes | str | None = None, ventana: str | None = None ) -> str:
   try:
        personalidad = get_config("personalidad") or "Eres Kira, una asistente directa."

        hechos = get_all_facts()
        texto_hechos = "\n- ".join(hechos) if hechos else "Ninguno aún."
        system_prompt = f"{personalidad}\nContexto de memoria (úsalo solo si el tema surge en la conversación, no lo repitas sin motivo):\n- {texto_hechos}"

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
                "num_predict": 250,
                "temperature": 0.55 if isinstance(imagen, list) else 0.45,
                "num_ctx": 4096,
            }
        )

        reply = answer['message']['content']

        if imagen is None:
            save_messages('user', prompt)
            save_messages('assistant', reply)

        return reply
   
   except Exception as e:
        import traceback
        traceback.print_exc()
        return f"An error occurred while connecting to Ollama: {e}"

async def extract_fact(message_user: str) -> None:
    try:
        text = message_user.strip()
        if len(text) < 12 or "?" in text:
            return

        prompt_extract = [
            {
                'role': 'system',
                'content': (
                    "Eres un filtro de memoria selectivo. Tu trabajo es extraer únicamente datos permanentes, biográficos, "
                    "de hardware o herramientas del usuario (como su nombre, sistema operativo, lenguajes o gustos fijos).\n"
                    "REGLAS:\n"
                    "- IGNORA por completo pruebas temporales, errores, saludos o charlas casuales (ej: 'estoy probando SQLite' -> NADA).\n"
                    "- GUARDA SÓLO si el mensaje aporta un hecho definitivo (ej: 'uso Windows 11' o 'me llamo Esteban' -> extráelo en una oración clara).\n"
                    "- Si no hay ningún dato permanente nuevo, responde únicamente: NADA"
                ),
            },
            {'role': 'user', 'content': text},
        ]
        
        res = await AsyncClient().chat(
            model="qwen2.5vl:3b",
            messages=prompt_extract,
            options={"temperature": 0.0, "num_predict": 40},
        )

        hecho = res['message']['content'].strip()
        if hecho and "NADA" not in hecho.upper() and len(hecho) <= 120:
            save_fact("auto", hecho)
    except Exception:
        pass