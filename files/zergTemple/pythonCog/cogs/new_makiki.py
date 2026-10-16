import discord
from discord.ext import commands

class NewMakikiCog(commands.Cog, name="New Makiki Retail"):
    def __init__(self, bot):
        self.bot = bot
        # Map your partner networks to brand IDs or tracking endpoints
        self.partners = {
            "REI": {"category": "Outdoor & Field", "color": 0x1B4D3E},
            "Apple": {"category": "Hardware & Tech", "color": 0xA2AAAD},
            "Nordstrom": {"category": "Apparel & Design", "color": 0x000000},
            "Target": {"category": "General Goods", "color": 0xCC0000},
            "Clack!PHX": {"category": "Local Hardware & Goods", "color": 0x9D4EDD}
        }
        # Target channel ID for automated retail drops (Update with your actual channel ID)
        self.retail_channel_id = 000000000000000000

    @commands.group(name="makiki", invoke_without_command=True)
    async def makiki(self, ctx):
        """New Makiki retail management base command."""
        embed = discord.Embed(
            title="🛍️ New Makiki Retail Ecosystem",
            description="Manage and broadcast partner brand integrations across the network.",
            color=0x9D4EDD
        )
        partner_list = "\n".join([f"• **{name}** — {info['category']}" for name, info in self.partners.items()])
        embed.add_field(name="Active Partner Network", value=partner_list, inline=False)
        embed.set_footer(text="Use `!makiki drop [partner] [item]` to broadcast a release.")
        await ctx.send(embed=embed)

    @makiki.command(name="drop", help="Broadcasts a new consumer goods drop from a partner network.")
    @commands.is_owner()
    async def makiki_drop(self, ctx, partner: str, *, item_details: str):
        """Simulates a product release notification for a partner company."""
        partner_key = next((p for p in self.partners if p.lower() == partner.lower()), None)
        
        if not partner_key:
            await ctx.send(f"❌ Unknown partner. Choose from: {', '.join(self.partners.keys())}")
            return

        partner_data = self.partners[partner_key]
        
        embed = discord.Embed(
            title=f"🚨 New Makiki Drop | {partner_key}",
            description=f"**Item:** {item_details}",
            color=partner_data["color"]
        )
        embed.add_field(name="Sector", value=partner_data["category"], inline=True)
        embed.add_field(name="Status", value="Available for Order / Sync", inline=True)
        embed.set_footer(text="New Makiki Retail Pipeline • Zerg Temple PHX")

        # Send to designated retail channel or current context if not set
        target_channel = self.bot.get_channel(self.retail_channel_id) or ctx.channel
        await target_channel.send(embed=embed)
        
        if target_channel != ctx.channel:
            await ctx.send(f"✅ Drop successfully broadcasted to <#{target_channel.id}>", delete_after=5)

async def setup(bot):
    await bot.add_cog(NewMakikiCog(bot))
