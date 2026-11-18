import re

from src.database import save_fact

PATRONES_BASURA = re.compile(
    r"^(kill|sudo|rm|ls|cd|git|exit|ping)\b"
    r"|^\s*!"                                 
    r"|\b(cómo|qué|cuándo|dónde|quién|por qué)\b", 
    re.IGNORECASE
)
PATRONES_RELEVANTES = {
    "identidad": re.compile(r"\b(me llamo|mi nombre es|puedes decirme|llámame)\b", re.IGNORECASE),
    "entorno": re.compile(r"\b(uso linux|uso windows|mi pc tiene| mi editor es|programo en| trabajo con)\b", re.IGNORECASE),
    "preferencias": re.compile(r"\b(me gusta|prefiero|odio|no me gusta)\b", re.IGNORECASE)
}

async def extract_fact(message_content: str) -> None:
    if not message_content or not  message_content.strip():
        return

    text = message_content.strip()

    # CLASIFICACION NIVEL 1 (INFORMACION IRRELEVANTE) NO SE GUARDAN EN LA BASE DE DATOS
    if len(text) < 5 or "?" in text or PATRONES_BASURA.search(text):
        return

    #CLASIFICACION NIVEL 2 (INFORMACION RELEVANTE) SI SE GUARDAN EN LA BASE DE DATOS
    for categoria, patron in PATRONES_RELEVANTES.items():
        if patron.search(text):
            save_fact(categoria, text)
            break