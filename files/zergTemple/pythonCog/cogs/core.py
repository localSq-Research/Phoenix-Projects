import discord
from discord.ext import commands

class CoreCog(commands.Cog, name="Core"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Checks the latency of the Zerg Temple PHX network.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="⚡ Zerg Temple PHX Status",
            description=f"Swarm operational. Latency: **{latency}ms**",
            color=0x9D4EDD
        )
        await ctx.send(embed=embed)

    @commands.command(name="reload", help="Reloads a specific cog extension dynamically.")
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully reloaded extension: `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Error reloading `cogs.{cog}`: `{e}`")

async def setup(bot):
    await bot.add_cog(CoreCog(bot))
