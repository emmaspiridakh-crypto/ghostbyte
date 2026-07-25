"""
cogs/autorole.py
------------------
Αυτόματος ρόλος: μόλις μπαίνει κάποιος στο server, παίρνει αυτόματα
τα role(s) που έχεις ορίσει στο config.AUTO_ROLE_IDS — χωρίς κουμπί,
χωρίς καμία ενέργεια από τον χρήστη.
"""

from __future__ import annotations

import discord
from discord.ext import commands

import config
from emojis import emoji
from utils import logs as logutil


class AutoRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role_ids = [rid for rid in config.AUTO_ROLE_IDS if rid]
        if not role_ids:
            return

        roles = [member.guild.get_role(rid) for rid in role_ids]
        roles = [r for r in roles if r is not None]
        if not roles:
            return

        try:
            await member.add_roles(*roles, reason="Auto role on join")
        except discord.Forbidden:
            return

        await logutil.log(
            member.guild, "role",
            title=f"{emoji('logs', 'role') or '➕'} Auto Role Assigned",
            color=0x57F287,
            fields=[
                ("User", f"{member.mention} (`{member.id}`)", False),
                ("Roles", ", ".join(r.mention for r in roles), False),
            ],
            thumbnail_url=member.display_avatar.url,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoRole(bot))
