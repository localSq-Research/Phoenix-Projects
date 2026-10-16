import discord
from discord.ext import commands

class ThroneCog(commands.Cog, name="Throne Integration"):
    def __init__(self, bot):
        self.bot = bot
        # Target channel ID for incoming contributions (Update with your actual channel ID)
        self.tribute_channel_id = 000000000000000000

    async def send_tribute_alert(self, supporter_name: str, item_name: str, message: str = None):
        """Helper method to trigger a formatted swarm contribution alert."""
        channel = self.bot.get_channel(self.tribute_channel_id)
        if not channel:
            return

        embed = discord.Embed(
            title="🎁 New Swarm Contribution!",
            description="A new item has been secured via the Throne wishlist pipeline.",
            color=0x00F0FF
        )
        embed.add_field(name="Operative", value=supporter_name, inline=True)
        embed.add_field(name="Item Acquired", value=item_name, inline=True)
        
        if message:
            embed.add_field(name="Transmission", value=f'"{message}"', inline=False)
            
        embed.set_footer(text="Zerg Temple PHX • Infrastructure Support")
        await channel.send(embed=embed)

    @commands.command(name="simulatereward", help="Test the Throne notification embed locally.")
    @commands.is_owner()
    async def simulate_reward(self, ctx, supporter: str, *, item: str):
        """Test command to verify webhook display formatting."""
        await self.send_tribute_alert(supporter_name=supporter, item_name=item, message="Keep building out the PHX tech infrastructure!")
        await ctx.send("Test tribute alert dispatched.", delete_after=5)

async def setup(bot):
    await bot.add_cog(ThroneCog(bot))
