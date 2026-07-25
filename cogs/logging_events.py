"""
cogs/logging_events.py
------------------------
Παρακολουθεί events που συμβαίνουν φυσικά στον server (όχι μέσω bot command)
και τα καταγράφει στο σωστό log channel:
  - Voice join / leave / move
  - Channel create / delete / update (rename)
  - Message edit / delete
  - Role assign / remove σε member (μέσω on_member_update)
"""

from __future__ import annotations

import discord
from discord.ext import commands

from emojis import emoji
from utils import logs as logutil


class LoggingEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Voice ────────────────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel == after.channel:
            return

        if before.channel is None and after.channel is not None:
            await logutil.log(
                member.guild, "voice",
                title=f"{emoji('logs', 'voice_join') or '🔊'} Voice Join",
                color=0x57F287,
                fields=[("User", member.mention, True), ("Channel", after.channel.mention, True)],
                thumbnail_url=member.display_avatar.url,
            )
        elif before.channel is not None and after.channel is None:
            await logutil.log(
                member.guild, "voice",
                title=f"{emoji('logs', 'voice_leave') or '🔇'} Voice Leave",
                color=0xED4245,
                fields=[("User", member.mention, True), ("Channel", before.channel.mention, True)],
                thumbnail_url=member.display_avatar.url,
            )
        else:
            await logutil.log(
                member.guild, "voice",
                title=f"{emoji('logs', 'voice_join') or '🔀'} Voice Move",
                color=0xFEE75C,
                fields=[
                    ("User", member.mention, True),
                    ("Από", before.channel.mention, True),
                    ("Σε", after.channel.mention, True),
                ],
                thumbnail_url=member.display_avatar.url,
            )

    # ── Channels ─────────────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        await logutil.log(
            channel.guild, "channel",
            title=f"{emoji('logs', 'channel') or '📁'} Channel Created",
            color=0x57F287,
            fields=[("Channel", f"{channel.mention if hasattr(channel, 'mention') else channel.name}", True),
                    ("Τύπος", str(channel.type), True)],
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        await logutil.log(
            channel.guild, "channel",
            title=f"{emoji('logs', 'channel') or '🗑️'} Channel Deleted",
            color=0xED4245,
            fields=[("Channel", f"#{channel.name}", True), ("Τύπος", str(channel.type), True)],
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if before.name == after.name:
            return
        await logutil.log(
            after.guild, "channel",
            title=f"{emoji('logs', 'channel') or '✏️'} Channel Renamed",
            color=0xFEE75C,
            fields=[("Πριν", before.name, True), ("Μετά", after.name, True)],
        )

    # ── Messages ─────────────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return
        await logutil.log(
            message.guild, "message",
            title=f"{emoji('logs', 'message') or '🗑️'} Message Deleted",
            color=0xED4245,
            fields=[
                ("Author", message.author.mention, True),
                ("Channel", message.channel.mention, True),
                ("Περιεχόμενο", (message.content or "*[χωρίς κείμενο / attachment]*")[:1000], False),
            ],
            thumbnail_url=message.author.display_avatar.url,
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot or before.guild is None:
            return
        if before.content == after.content:
            return
        await logutil.log(
            after.guild, "message",
            title=f"{emoji('logs', 'message') or '✏️'} Message Edited",
            color=0xFEE75C,
            fields=[
                ("Author", after.author.mention, True),
                ("Channel", after.channel.mention, True),
                ("Πριν", (before.content or "—")[:500], False),
                ("Μετά", (after.content or "—")[:500], False),
            ],
            thumbnail_url=after.author.display_avatar.url,
        )

    # ── Roles ────────────────────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        before_roles = set(before.roles)
        after_roles = set(after.roles)
        added = after_roles - before_roles
        removed = before_roles - after_roles

        for role in added:
            await logutil.log(
                after.guild, "role",
                title=f"{emoji('logs', 'role') or '➕'} Role Added",
                color=0x57F287,
                fields=[("User", after.mention, True), ("Role", role.mention, True)],
                thumbnail_url=after.display_avatar.url,
            )
        for role in removed:
            await logutil.log(
                after.guild, "role",
                title=f"{emoji('logs', 'role') or '➖'} Role Removed",
                color=0xED4245,
                fields=[("User", after.mention, True), ("Role", role.mention, True)],
                thumbnail_url=after.display_avatar.url,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(LoggingEvents(bot))
