import discord
from discord.ext import commands
from discord import Interaction, app_commands, Embed
from pymongo import MongoClient

# ==== CONFIG ====
TOKEN = "YOUR_BOT_TOKEN_HERE"
MONGO_URI = "YOUR_MONGEDB_URL" #This should be something like: mongodb+srv://NAME:PASS@HOST/
# =================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# MongoDB client
client = MongoClient(MONGO_URI)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online als {bot.user}")

@bot.tree.command(name="showdb")
async def show_databases(interaction: Interaction):
    """Toont alle databases en collecties in MongoDB."""
    databases = client.list_database_names()
    response = "**📂 Databases en Collecties in MongoDB:**\n"
    
    for db_name in databases:
        db = client[db_name]
        collections = db.list_collection_names()
        response += f"\n`{db_name}`:\n"
        for coll in collections:
            response += f"  - {coll}\n"
    
    if len(response) > 1900:  # Discord limit
        await interaction.response.send_message("Too much data to show in one message. (Discord limit)")
    else:
        await interaction.response.send_message(response)

@bot.tree.command(name="showcoll")
async def show_collection(interaction: Interaction, db_name: str):
    """Toont alle documenten in een collectie (max 10)."""
    interaction.defer()
    if db_name not in client.list_database_names():
        await interaction.followup.send(f"Database `{db_name}` bestaat niet.")
        return
    
    db = client[db_name]
    collections = db.list_collection_names()
    response = f"**📂 Collecties in `{db_name}`:**\n"
    for coll in collections:
        response += f"- {coll}\n"
    
    await interaction.followup.send(response)

@bot.tree.command(name="", desctiption="View te author"

bot.run(TOKEN)
