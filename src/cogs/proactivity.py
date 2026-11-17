import random

from datetime import datetime

from discord.ext import commands, tasks
from src.ollama_client import consult
from src.proactivity.inactivity_manager import InactivityManager

class ProActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.inactivity = InactivityManager(downtime=60, cooldown=120)
        self.monitor_inactivity.start()

    def cog_unload(self):
        self.monitor_inactivity.cancel()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.owner_id:
            self.inactivity.log_interaction()

    @tasks.loop(seconds=20)
    async def monitor_inactivity(self):
        if not self.bot.ultimo_canal:
            return

        if self.inactivity.must_speak():
            hora = datetime.now().hour
            ideas = [
                    "Manda un mensaje de una sola línea preguntando en qué andas.",
                    "Haz un comentario muy corto y casual sobre código o tecnología.",
                    "Saluda en una frase corta y directa, como un amigo en Discord.",
                    "Saca un tema breve basado en lo que sabes del Jefe, sin sonar formal.",
            ]
            enfoque_elegido = random.choice(ideas)

            prompt_system = (
                 f"[INICIATIVA PROPIA: {enfoque_elegido} "
                "Responde en máximo 1 o 2 oraciones cortas. Prohibido sonar como soporte técnico.]"
            )
            async with self.bot.ultimo_canal.typing():
                answer = await consult(prompt_system)
                if answer and answer.strip():
                    await self.bot.ultimo_canal.send(answer)

    @monitor_inactivity.before_loop
    async def before_monitor(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(ProActivityCog(bot))