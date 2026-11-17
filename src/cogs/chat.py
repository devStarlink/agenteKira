import discord
import asyncio
import re

from discord.ext import commands

from src.extract_manager import extract_fact
from src.ollama_client import consult
from src.vision_engine import take_screenshot
from src.database import save_fact

PATRON_VISION = re.compile(
     r"\b(mir|ve|chec|revis|observ|analiz)[a-z]*\b.*\b(pantalla|pantallas|monitor|monitores|escritorio)\b"
     r"|\b(pantalla|pantallas|monitor|monitores|escritorio)\b.*\b(mir|ve|chec|revis|observ|analiz)[a-z]*\b",
     re.IGNORECASE,
)

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.id != self.bot.owner_id:
            print(f"[ALERTA] Acceso bloqueado de: {message.author} (ID: {message.author.id})")
            return

        if message.content.startswith("!") or not message.content.strip():
            return

        disparadores_memoria = ("recuerda que ", "guarda que ", "anota que ", "memoriza que ")
        texto_minuscula = message.content.lower().strip()

        guardado_manual = False

        for disparador in disparadores_memoria:
            if texto_minuscula.startswith(disparador):
                dato_nuevo = message.content.strip()[len(disparador):].strip()
                if dato_nuevo:
                    save_fact("aprendido", f"el usario indicó: {dato_nuevo}")
                    guardado_manual = True

        capture = take_screenshot() if PATRON_VISION.search(message.content) else None

        imagen = None
        ventana = None

        if isinstance(capture, tuple):
            imagen, ventana = capture

        elif isinstance(capture, str) and capture == "BLOQUEADO":
            imagen = "BLOQUEADO"
            ventana = None

        async with message.channel.typing():
            answer = await consult(message.content, imagen=imagen, ventana=ventana)
            if not answer or not answer.strip():
                answer = "Tsk, me quedé en blanco. Repítemelo."
            await message.channel.send(answer)

            if not message.author.bot and not guardado_manual:
                asyncio.create_task(extract_fact(message.content))

async def setup(bot):
    await bot.add_cog(ChatCog(bot))