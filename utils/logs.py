"""
utils/logs.py
--------------
Κεντρικό σύστημα logging. Κάθε κατηγορία (voice, channel, message, role,
ticket, ban, unban, timeout, untimeout, kick, mod, giveaway) πάει στο δικό
της channel, όπως ορίζεται στο config.LOG_CHANNELS.
"""

from __future__ import annotations
import datetime
import discord

import config


def build_log_embed(
    *,
    title: str,
    color: int,
    fields: list[tuple[str, str, bool]],
    thumbnail_url: str | None = None,
    guild: discord.Guild | None = None,
) -> discord.Embed:
    embed = discord.Embed(title=title, color=color, timestamp=datetime.datetime.now(datetime.timezone.utc))
    for name, value, inline in fields:
        embed.add_field(name=name, value=value or "—", inline=inline)
    thumb = thumbnail_url or config.LOG_THUMBNAIL_URL
    if thumb:
        embed.set_thumbnail(url=thumb)
    if guild and guild.icon:
        embed.set_footer(text=guild.name, icon_url=guild.icon.url)
    return embed


async def send_log(guild: discord.Guild, category: str, embed: discord.Embed):
    """Στέλνει το embed στο σωστό log channel βάσει κατηγορίας."""
    if guild is None:
        return
    channel_id = config.LOG_CHANNELS.get(category)
    if not channel_id:
        return
    channel = guild.get_channel(channel_id)
    if channel is None:
        return
    try:
        await channel.send(embed=embed)
    except discord.HTTPException:
        pass


async def log(
    guild: discord.Guild,
    category: str,
    *,
    title: str,
    color: int,
    fields: list[tuple[str, str, bool]],
    thumbnail_url: str | None = None,
):
    """Shortcut: φτιάχνει το embed και το στέλνει στο σωστό log channel."""
    embed = build_log_embed(title=title, color=color, fields=fields, thumbnail_url=thumbnail_url, guild=guild)
    await send_log(guild, category, embed)
