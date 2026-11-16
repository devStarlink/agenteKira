import os

from pathlib import Path
from dotenv import load_dotenv

from src.database import database_creation, get_config, save_config, save_fact, get_all_facts

def check_setup() -> None:
    database_creation()
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    owner_id = os.getenv("MY_USER_ID")

    if not token or not owner_id:
        while not token:
            token = input("Ingresa el token de tu bot de Discord: ").strip()

        while not owner_id:
            owner_id = input("Ingresa tu ID de usuario de Discord: ").strip()

        Path(".env").write_text(f"DISCORD_TOKEN={token}\nMY_USER_ID={owner_id}\n", encoding="utf-8")
        load_dotenv(override=True)

    personalidad = get_config("personalidad")

    if not personalidad:
        personalidad = input("Escribe y describe la personalidad de kira (INCLUYA PROHIBICIONES COMO CERO MULETIÑAS O RESPUESTAS GENERICAS): ").strip()

        if not personalidad:
            personalidad = "Eres kira, tu personalidad se describe como calmada, dispuesta ayudar y sin respuestas ambiguas ni artificiales"

    save_config("personalidad", personalidad)

    if not get_all_facts():
        name_user = input("¿Como quieres que te llame a ti desde ahora? (Enter para omitir) ").strip()

        if name_user:
            save_fact("usuario", f"El usuario con el que hablas se llama {name_user}. Tú eres Kira y debes llamarlo {name_user} a él.")

        proposito = ""
        while not proposito:
            proposito = input("¿Cuál es el propósito principal de Kira? (Obligatorio): ").strip()
        save_fact("proposito", f"Mi propósito principal es: {proposito}.")
        
        habilidades = input("¿Qué sabe hacer kira? (Enter para usar capacidades base) ").strip()
        if not habilidades:
            habilidades = "Conversar en Discord, analizar capturas de pantalla en tiempo real y proteger la privacidad bloqueando datos sensibles."
        save_fact("capacidades", f"Mis Capacidades instaladas son: {habilidades}")