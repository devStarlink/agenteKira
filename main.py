import os 

from dotenv import load_dotenv

from src.bot_core import iniciar_bot
from src.setup_wizard import check_setup


def main():
    check_setup()
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    owner_id_str = os.getenv("MY_USER_ID")
    
    if not token or not owner_id_str:
        print("¡Error! Faltan credenciales en el .env")
        return

    owner_id = int(owner_id_str)
    print("Despertando a Kira...")
    iniciar_bot(token=token, owner_id=owner_id)

if __name__ == "__main__":
    main()