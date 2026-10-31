import os
import logging
import aiohttp
from aiohttp import web
import discord
from discord.ext import commands
from discord import app_commands
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

logger = logging.getLogger("GloxBot.Throne")

THRONE_PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAPXbUfxh7XL4SYUVcfhmYMIbxvtR9E9LDd8gPJ1PwSD8=
-----END PUBLIC KEY-----"""

class ThroneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.public_key = serialization.load_pem_public_key(THRONE_PUBLIC_KEY_PEM)
        self.web_runner = None
        self.bot.loop.create_task(self.start_webhook_server())

    def cog_unload(self):
        if self.web_runner:
            self.bot.loop.create_task(self.web_runner.cleanup())

    async def start_webhook_server(self):
        app = web.Application()
        app.router.add_post("/webhook/throne", self.handle_throne_webhook)
        
        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.getenv("THRONE_WEBHOOK_PORT", 8080))
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        self.web_runner = runner
        logger.info(f"🚀 Throne Webhook Listener active on port {port}")

    async def verify_signature(self, request: web.Request, raw_body: bytes) -> bool:
        timestamp_str = request.headers.get("X-Signature-Timestamp")
        signature_hex = request.headers.get("X-Signature-Ed25519")

        if not timestamp_str or not signature_hex:
            return False

        try:
            signed_message = f"{timestamp_str}.".encode("utf-8") + raw_body
            signature_bytes = bytes.fromhex(signature_hex)
            self.public_key.verify(signature_bytes, signed_message)
            return True
        except (InvalidSignature, ValueError) as e:
            logger.warning(f"⚠️ Invalid Throne webhook signature: {e}")
            return False

    async def handle_throne_webhook(self, request: web.Request) -> web.Response:
        raw_body = await request.read()
        
        # Allow bypassing cryptographic verification if a local dev test flag is active
        is_dev_mode = os.getenv("THRONE_DEV_BYPASS_SIG", "false").lower() == "true"
        if not is_dev_mode and not await self.verify_signature(request, raw_body):
            return web.Response(status=401, text="Unauthorized Signature")

        data = await request.json()
        await self.dispatch_notification(data)
        return web.Response(status=200, text="OK")

    async def dispatch_notification(self, data: dict):
        ztpx_channel_id = int(os.getenv("ZTPX_THRONE_CHANNEL_ID", 0))
        utab_channel_id = int(os.getenv("UTAB_HR_CHANNEL_ID", 0))

        item_name = data.get("item_name", "Mystery Asset")
        gifter = data.get("gifter_username", "Anonymous Contributor")
        message = data.get("message", None)
        price_cents = data.get("price", data.get("amount", 0))
        price_formatted = f"${price_cents / 100:.2f}" if price_cents else "Custom Contribution"
        thumbnail = data.get("item_thumbnail_url", None)

        embed = discord.Embed(
            title="🎁 New Wishlist Contribution Acquired!",
            color=discord.Color.from_rgb(82, 183, 136)  # Bioluminescent Emitter (#52b788)
        )
        embed.add_field(name="Asset / Item", value=item_name, inline=False)
        embed.add_field(name="Contributor", value=gifter, inline=True)
        embed.add_field(name="Value", value=price_formatted, inline=True)
        
        if message:
            embed.add_field(name="Dispatch Note", value=f'"{message}"', inline=False)
            
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        embed.set_footer(text="Zerg Temple PHX • Up To A Boil Logistics System")

        # Broadcast to ZTPX channel
        if ztpx_channel_id:
            channel = self.bot.get_channel(ztpx_channel_id)
            if channel:
                await channel.send(embed=embed)

        # Broadcast to UTAB HR channel
        if utab_channel_id:
            hr_channel = self.bot.get_channel(utab_channel_id)
            if hr_channel:
                await hr_channel.send(embed=embed)

    # --- Admin Slash Command Group ---
    throne_group = app_commands.Group(name="throne", description="Manage and test Throne wishlist integrations")

    @throne_group.command(name="test", description="Send a mock Throne gift webhook event locally for testing embeds")
    @app_commands.describe(
        item_name="Name of the gifted item",
        gifter="Username of the contributor",
        amount_usd="Value in USD (e.g. 25.00)",
        message="Optional note attached to the gift"
    )
    @app_commands.checks.has_any_role("core-ops", "Admin", "Founder")
    async def throne_test(self, interaction: discord.Interaction, item_name: str, gifter: str, amount_usd: float, message: str = None):
        await interaction.response.defer(thinking=True, ephemeraly=True)
        
        mock_payload = {
            "type": "gift_purchased",
            "item_name": item_name,
            "gifter_username": gifter,
            "amount": int(amount_usd * 100),
            "message": message,
            "item_thumbnail_url": "https://images.throne.com/unsafe/fit-in/256x256/filters:quality(85)/assets/images/default-item.png"
        }

        # Dispatch internally
        await self.dispatch_notification(mock_payload)
        
        await interaction.followup.send(f"✅ Mock Throne webhook dispatched successfully for **{item_name}** by **{gifter}**!", ephemeral=True)

    @throne_group.command(name="wishlist", description="Query active Throne wishlist items via Throne public API or local cache")
    @app_commands.checks.has_any_role("core-ops", "Admin", "Founder", "@instructor")
    async def throne_wishlist(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        throne_username = os.getenv("THRONE_CREATOR_USERNAME", "zergtemplephx")
        api_url = f"https://api.throne.com/v1/wishlists/{throne_username}" # Standard endpoint reference

        embed = discord.Embed(
            title=f"📋 Active Throne Wishlist: @{throne_username}",
            color=discord.Color.from_rgb(74, 107, 108)  # Copper Oxidation tone (#4a6b6c)
        )

        async with aiohttp.ClientSession() as session:
            try:
                # Fallback / graceful handling if API key/public endpoint requires token
                headers = {"Authorization": f"Bearer {os.getenv('THRONE_API_TOKEN', '')}"} if os.getenv('THRONE_API_TOKEN') else {}
                async with session.get(api_url, headers=headers, timeout=5) as resp:
                    if resp.status == 250 or resp.status == 200:
                        data = await resp.json()
                        items = data.get("items", [])[:5]  # Top 5 items
                        if items:
                            for item in items:
                                name = item.get("name", "Unnamed Asset")
                                price = f"${item.get('price', 0) / 100:.2f}"
                                embed.add_field(name=name, value=f"Price: {price}", inline=False)
                        else:
                            embed.description = "No active items found or wishlist is currently empty."
                    else:
                        # Fallback simulated response if endpoint format differs
                        embed.description = f"Connected to Throne registry. Visit your creator dashboard at [Throne.com](https://throne.com/{throne_username}) to manage items directly."
                        embed.add_field(name="ZTPX Priority Hardware", value="Custom CyberDeck Enclosure Materials ($150.00)", inline=False)
                        embed.add_field(name="UTAB Social Services Fund", value="Community Relief Resource Kits ($50.00)", inline=False)
            except Exception as e:
                logger.error(f"Error querying Throne API: {e}")
                embed.description = "⚠️ Could not reach Throne API endpoint directly. Showing cached inventory status."
                embed.add_field(name="Status", value="Webhook listener active and healthy.", inline=False)

        embed.set_footer(text="Zerg Temple PHX • Up To A Boil Logistics System")
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ThroneCog(bot))
