import asyncio
import os
import discord
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
CHANNEL_ID = 123456789012345678  # The Discord channel ID where the status board lives

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

twitch_client = None
status_message_id = None  # Track the persistent message ID

async def get_users_from_database():
    """
    Placeholder for your database connection/query.
    Returns a list of dictionaries or tuples containing Twitch usernames.
    """
    # Example mock data representing your database records:
    return [{"twitch_username": "streamer_one"}, {"twitch_username": "streamer_two"}]

@bot.event
async def on_ready():
    global twitch_client
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    # Initialize Twitch API client (App Authentication)
    twitch_client = await Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    
    # Start the background status loop
    check_twitch_status.start()

@tasks.loop(minutes=3.0)
async def check_twitch_status():
    global status_message_id
    if not twitch_client:
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Target channel {CHANNEL_ID} not found.")
        return

    # 1. Fetch user list from database
    db_users = await get_users_from_database()
    usernames = [user["twitch_username"] for user in db_users]
    
    if not usernames:
        return

    try:
        # 2. Query Twitch API (Twitch allows batches of up to 100 user logins)
        live_streams = []
        # Chunk into groups of 100 if your database is large
        async for stream in twitch_client.get_streams(user_login=usernames):
            live_streams.append(stream)
            
        # 3. Build the Discord Embed
        embed = discord.Embed(
            title="🔴 Community Live Status Board",
            description="Active streams from our database:",
            color=discord.Color.purple()
        )
        
        if live_streams:
            for stream in live_streams:
                embed.add_field(
                    name=stream.user_name,
                    value=f"🎮 **Game:** {stream.game_name or 'Not specified'}\n"
                          f"👥 **Viewers:** {stream.viewer_count}\n"
                          f"💬 [{stream.title}]({f'https://twitch.tv/{stream.user_login}'})",
                    inline=False
                )
        else:
            embed.add_field(name="Status", value="No tracked users are currently live.", inline=False)
            
        embed.set_footer(text="Auto-refreshed every 3 minutes")

        # 4. Handle Persistent Messaging (Edit existing message or post a new one)
        if status_message_id:
            try:
                msg = await channel.fetch_message(status_message_id)
                await msg.edit(embed=embed)
                return
            except discord.NotFound:
                # Message was deleted manually, clear ID to send a new one
                status_message_id = None

        # Send a fresh message if none exists
        new_msg = await channel.send(embed=embed)
        status_message_id = new_msg.id

    except Exception as e:
        print(f"Error updating Twitch status board: {e}")

@check_twitch_status.before_loop
async def before_check_twitch_status():
    await bot.wait_until_ready()

# Run the bot
bot.run(DISCORD_TOKEN)
