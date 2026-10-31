import os
import logging
from aiohttp import web
import discord
from discord.ext import commands
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

logger = logging.getLogger("GloxBot.Throne")

# Throne Public Key (PEM format provided by Throne API docs)
THRONE_PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAPXbUfxh7XL4SYUVcfhmYMIbxvtR9E9LDd8gPJ1PwSD8=
-----END PUBLIC KEY-----"""

class ThroneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pub_key = Ed25519PublicKey.from_public_bytes(
            # Extract raw 32 bytes from PEM if needed, or initialize properly.
            # Alternatively, using cryptography's serialization:
        )
        # Let's load the public key correctly using serialization
        from cryptography.hazmat.primitives import serialization
        self.public_key = serialization.load_pem_public_key(THRONE_PUBLIC_KEY_PEM)
        
        # Start background aiohttp web app listener for webhooks if not already bound
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
            # Build signed message: M = T + "." + B
            signed_message = f"{timestamp_str}.".encode("utf-8") + raw_body
            signature_bytes = bytes.fromhex(signature_hex)
            
            self.public_key.verify(signature_bytes, signed_message)
            return True
        except (InvalidSignature, ValueError) as e:
            logger.warning(f"⚠️ Invalid Throne webhook signature: {e}")
            return False

    async def handle_throne_webhook(self, request: web.Request) -> web.Response:
        raw_body = await request.read()
        
        if not await self.verify_signature(request, raw_body):
            return web.Response(status=401, text="Unauthorized Signature")

        data = await request.json()
        event_type = data.get("type", "gift_purchased") # depending on payload structure
        
        await self.dispatch_notification(data)
        return web.Response(status=200, text="OK")

    async def dispatch_notification(self, data: dict):
        # Determine target channels based on config or guild mapping
        # Zerg Temple PHX channel ID vs Up To A Boil HR channel ID
        ztpx_channel_id = int(os.getenv("ZTPX_THRONE_CHANNEL_ID", 0))
        utab_channel_id = int(os.getenv("UTAB_HR_CHANNEL_ID", 0))

        item_name = data.get("item_name", "Mystery Asset")
        gifter = data.get("gifter_username", "Anonymous")
        message = data.get("message", None)
        price_cents = data.get("price", data.get("amount", 0))
        price_formatted = f"${price_cents / 100:.2f}" if price_cents else "Custom Contribution"
        thumbnail = data.get("item_thumbnail_url", None)

        embed = discord.Embed(
            title="🎁 New Wishlist Contribution Acquired!",
            color=discord.Color.from_rgb(82, 183, 136) # Bioluminescent Emitter palette tone (#52b788)
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

        # Broadcast to UTAB HR channel if social services / company funds impacted
        if utab_channel_id:
            hr_channel = self.bot.get_channel(utab_channel_id)
            if hr_channel:
                await hr_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ThroneCog(bot))
