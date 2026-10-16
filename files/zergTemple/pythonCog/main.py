import asyncio
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Zerg Temple PHX Ecosystem Online.")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded extension: {filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        # Insert your bot token here or via environment variable
        await bot.start(os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
