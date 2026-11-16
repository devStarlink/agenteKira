import discord
import asyncio

from discord.ext import commands

from src.ollama_client import consult, extract_fact
from src.vision_engine import take_screenshot
from src.database import save_fact

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

        pistas = ("mira", "ves", "pantalla", "ayuda", "vez", "miras", "que tal ahora")
        capture = take_screenshot() if any(p in message.content.lower() for p in pistas) else None

        if isinstance(capture, tuple):
            imagen, ventana = capture
        else:
            imagen, ventana = capture, None

        async with message.channel.typing():
            answer = await consult(message.content, imagen=imagen, ventana=ventana)
            if not answer or not answer.strip():
                answer = "Tsk, me quedé en blanco. Repítemelo."
            await message.channel.send(answer)

            if not guardado_manual:
                asyncio.create_task(extract_fact(message.content))

async def setup(bot):
    await bot.add_cog(ChatCog(bot))