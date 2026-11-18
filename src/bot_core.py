import discord
from discord.ext import commands

class KiraBot(commands.Bot):
    def __init__(self, owner_id: int):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)
        self.owner_id = owner_id
        self.ultimo_canal = None

    async def setup_hook(self):
        await self.load_extension("src.cogs.voice")
        print("[MODULOS] Módulo de voz cargado exitosamente.")

        await self.load_extension("src.cogs.chat")
        print("[MODULOS] Módulo de chat cargado exitosamente.")

        await self.load_extension("src.cogs.proactivity")
        print("[MODULOS] Módulo de proactividad cargado exitosamente.")

    async def on_ready(self):
        print(f"[OK] {self.user} conectado y operando bajo aislamiento estricto.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.author.id != self.owner_id:
            print(f"[ALERTA] Acceso bloqueado de: {message.author} (ID: {message.author.id})")
            return

        self.ultimo_canal = message.channel

        await self.process_commands(message)

def iniciar_bot(token: str, owner_id: int):
    bot = KiraBot(owner_id=owner_id)
    bot.run(token)