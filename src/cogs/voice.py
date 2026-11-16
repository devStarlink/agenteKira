import discord
from discord.ext import commands

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="entrar", help="Hace que Kira se meta a tu canal de voz.")
    async def entrar(self, ctx: commands.Context):
        # Revisa si el usuario que manda el comando está conectado a un canal de voz
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("¡Ey! Tienes que estar metido en un canal de voz primero para que pueda acompañarte.")
            return

        canal_destino = ctx.author.voice.channel

        # Si el bot ya está conectado en otro canal, se mueve; si no, se conecta
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(canal_destino)
            await ctx.send(f"Me mudé al canal de voz: **{canal_destino.name}**.")
        else:
            await canal_destino.connect()
            await ctx.send(f"Conectada al canal de voz: **{canal_destino.name}**.")

    @commands.command(name="salir", help="Saca a Kira del canal de voz.")
    async def salir(self, ctx: commands.Context):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send("Me salí del canal de voz. ¡Hasta luego!")
        else:
            await ctx.send("No estoy en ningún canal de voz ahorita.")

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))