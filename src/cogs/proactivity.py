from discord.ext import commands, tasks
from src.ollama_client import consult
from src.proactivity.system_events import SystemEventsManager

class ProActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.system_events = SystemEventsManager(cooldown=3600)
        self.monitor_system_events.start()

    def cog_unload(self):
        self.monitor_system_events.cancel()

    @tasks.loop(seconds=10)
    async def monitor_system_events(self):
        if not self.bot.ultimo_canal:
            return

        detected_app = self.system_events.check_events()
        if detected_app:
            async with self.bot.ultimo_canal.typing():
                answer = await consult(
                    prompt=f"Dime un comentario corto y casual sobre {detected_app} porque lo acabo de abrir.",
                    save_to_history=False,
                    system_event=f"El Jefe (hombre) acaba de abrir {detected_app} en su PC. Hazle un comentario casual y natural de 1 sola oración sobre {detected_app}, sin ofrecer ayuda."
                )
                if answer and answer.strip():
                    await self.bot.ultimo_canal.send(answer)

    @monitor_system_events.before_loop
    async def before_system_monitor(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(ProActivityCog(bot))