"""
main.py
-------
Entry point του bot. Φορτώνει όλα τα cogs, ξεκινάει τον Flask keep-alive
server (για Render) και κάνει sync τα slash commands.
"""

from __future__ import annotations

import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands

import config
from keep_alive import keep_alive
from utils import db as turso_db

os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

COGS = [
    "cogs.verify",
    "cogs.autorole",
    "cogs.tickets",
    "cogs.welcome",
    "cogs.tos",
    "cogs.logging_events",
    "cogs.moderation",
    "cogs.reviews",
    "cogs.suggestions",
    "cogs.giveaways",
]


@bot.event
async def on_ready():
    print(f"[Bot] Συνδέθηκε ως {bot.user} ({bot.user.id})")
    try:
        if config.GUILD_ID:
            guild_obj = discord.Object(id=config.GUILD_ID)
            synced = await bot.tree.sync(guild=guild_obj)
        else:
            synced = await bot.tree.sync()
        print(f"[Bot] Sync-άρισε {len(synced)} slash commands.")
    except Exception as e:
        print(f"[Bot] Σφάλμα στο sync: {e}")


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingAnyRole) or isinstance(error, app_commands.MissingRole):
        msg = "⛔ Δεν έχεις δικαίωμα να χρησιμοποιήσεις αυτή την εντολή."
    else:
        msg = f"⚠️ Σφάλμα: {error}"

    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


async def main():
    keep_alive()
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"[Bot] Φορτώθηκε: {cog}")
            except Exception as e:
                print(f"[Bot] ΑΠΕΤΥΧΕ να φορτωθεί {cog}: {e}")
        try:
            await bot.start(config.BOT_TOKEN)
        finally:
            await turso_db.close()


if __name__ == "__main__":
    asyncio.run(main())
