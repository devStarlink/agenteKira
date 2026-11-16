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
                                        f"{system_prompt} Estás viendo la captura de pantalla del usuario. "
                                        "Describe en tercera persona qué aplicación o contenido ves en la imagen, "
                                        "en máximo 2 oraciones directas sin inventar historias ni hablar de programación si no hay código en pantalla."
                                   ),
        },
        {
            'role': 'user',
            'content': f"[Ventana activa: {ventana}]\n{prompt}",
            'images': imagen,
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
                    "Eres un extractor de memoria. Analiza el mensaje del usuario. "
                    "Si menciona un dato personal permanente, preferencia, gusto, proyecto o herramienta que usa, "
                    "resúmelo en UNA sola oración corta y objetiva (ejemplo: 'el usario toma cafe.'). "
                    "Si es un saludo, broma, orden momentánea o charla sin datos permanentes, responde únicamente: NADA"
                ),
            },

            {'role': 'user', 'content': text},

        ]
        res = await AsyncClient().chat(
            model="qwen2.5vl:3b",
            messages=prompt_extract,
            options={"temperature": 0.1, "num_predict": 35},
        )

        hecho = res['message']['content'].strip()
        if hecho and "NADA" not in hecho.upper() and len(hecho) <= 120:
            save_fact("auto", hecho)
    except Exception:
        pass