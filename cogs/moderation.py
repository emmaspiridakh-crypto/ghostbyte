"""
cogs/moderation.py
--------------------
Prefix (!) commands για CEO / CO-CEO:
  !ban <@user|id> [λόγος]
  !unban <id>
  !timeout <@user> <διάρκεια π.χ. 10m/1h/1d> [λόγος]
  !untimeout <@user>
  !kick <@user> [λόγος]
  !dmall <μήνυμα>            (μόνο CEO — στέλνει DM σε όλα τα members)
  !say <#channel> <μήνυμα>   (panel με thumbnail)
  !say2 <#channel> <τίτλος> | <μήνυμα>  (panel με thumbnail, με τίτλο)

Όλα καταγράφονται σε logs (ξεχωριστό channel ανά κατηγορία).
"""

from __future__ import annotations

import re
import datetime
import asyncio

import discord
from discord import ui
from discord.ext import commands

import config
from emojis import emoji
from utils.permissions import has_roles
from utils import logs as logutil


def mod_only():
    async def predicate(ctx: commands.Context) -> bool:
        if not isinstance(ctx.author, discord.Member):
            return False
        return has_roles(ctx.author, config.MOD_ROLE_IDS)
    return commands.check(predicate)


def ceo_only():
    async def predicate(ctx: commands.Context) -> bool:
        if not isinstance(ctx.author, discord.Member):
            return False
        return has_roles(ctx.author, [config.CEO_ROLE_ID])
    return commands.check(predicate)


def _parse_duration(text: str):
    pattern = r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?"
    m = re.fullmatch(pattern, text.strip().lower())
    if not m or not any(m.groups()):
        return None
    d, h, mins = (int(x) if x else 0 for x in m.groups())
    return datetime.timedelta(days=d, hours=h, minutes=mins)


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return True  # per-command checks below

    # ── Ban / Unban ───────────────────────────────────────────────────────────

    @commands.command(name="ban")
    @mod_only()
    async def ban_cmd(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Δεν δόθηκε λόγος"):
        try:
            await member.ban(reason=f"{reason} | by {ctx.author}")
        except discord.Forbidden:
            await ctx.reply("⚠️ Δεν έχεις δικαίωμα να κάνεις ban αυτόν τον χρήστη.")
            return
        await ctx.reply(f"✅ Ο/Η {member.mention} έγινε banned.")
        await logutil.log(
            ctx.guild, "ban",
            title=f"{emoji('logs', 'ban') or '🔨'} Member Banned",
            color=0xED4245,
            fields=[
                ("User", f"{member.mention} (`{member.id}`)", False),
                ("Λόγος", reason, False),
                ("Από", ctx.author.mention, True),
            ],
            thumbnail_url=member.display_avatar.url,
        )

    @commands.command(name="unban")
    @mod_only()
    async def unban_cmd(self, ctx: commands.Context, user_id: int, *, reason: str = "Δεν δόθηκε λόγος"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"{reason} | by {ctx.author}")
        except discord.NotFound:
            await ctx.reply("⚠️ Δεν βρέθηκε banned χρήστης με αυτό το ID.")
            return
        except discord.Forbidden:
            await ctx.reply("⚠️ Δεν έχεις δικαίωμα να κάνεις unban.")
            return
        await ctx.reply(f"✅ Ο/Η {user.mention} έγινε unbanned.")
        await logutil.log(
            ctx.guild, "unban",
            title=f"{emoji('logs', 'unban') or '🔓'} Member Unbanned",
            color=0x57F287,
            fields=[
                ("User", f"{user.mention} (`{user.id}`)", False),
                ("Λόγος", reason, False),
                ("Από", ctx.author.mention, True),
            ],
            thumbnail_url=user.display_avatar.url,
        )

    # ── Timeout / Untimeout ──────────────────────────────────────────────────

    @commands.command(name="timeout")
    @mod_only()
    async def timeout_cmd(self, ctx: commands.Context, member: discord.Member, duration: str, *, reason: str = "Δεν δόθηκε λόγος"):
        delta = _parse_duration(duration)
        if not delta:
            await ctx.reply("⚠️ Λάθος format διάρκειας. Χρήση: `10m`, `1h`, `1d`, `1h30m`")
            return
        try:
            await member.timeout(delta, reason=f"{reason} | by {ctx.author}")
        except discord.Forbidden:
            await ctx.reply("⚠️ Δεν έχεις δικαίωμα να κάνεις timeout αυτόν τον χρήστη.")
            return
        until = discord.utils.utcnow() + delta
        await ctx.reply(f"✅ Ο/Η {member.mention} πήρε timeout μέχρι {discord.utils.format_dt(until, style='R')}.")
        await logutil.log(
            ctx.guild, "timeout",
            title=f"{emoji('logs', 'timeout') or '🔇'} Member Timed Out",
            color=0xFEE75C,
            fields=[
                ("User", f"{member.mention} (`{member.id}`)", False),
                ("Διάρκεια", duration, True),
                ("Λόγος", reason, False),
                ("Από", ctx.author.mention, True),
            ],
            thumbnail_url=member.display_avatar.url,
        )

    @commands.command(name="untimeout")
    @mod_only()
    async def untimeout_cmd(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Δεν δόθηκε λόγος"):
        try:
            await member.timeout(None, reason=f"{reason} | by {ctx.author}")
        except discord.Forbidden:
            await ctx.reply("⚠️ Δεν έχω δικαίωμα.")
            return
        await ctx.reply(f"✅ Ο/Η {member.mention} δεν έχει πλέον timeout.")
        await logutil.log(
            ctx.guild, "untimeout",
            title=f"{emoji('logs', 'untimeout') or '🔊'} Timeout Removed",
            color=0x57F287,
            fields=[
                ("User", f"{member.mention} (`{member.id}`)", False),
                ("Λόγος", reason, False),
                ("Από", ctx.author.mention, True),
            ],
            thumbnail_url=member.display_avatar.url,
        )

    # ── Kick ─────────────────────────────────────────────────────────────────

    @commands.command(name="kick")
    @mod_only()
    async def kick_cmd(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Δεν δόθηκε λόγος"):
        try:
            await member.kick(reason=f"{reason} | by {ctx.author}")
        except discord.Forbidden:
            await ctx.reply("⚠️ Δεν έχεις δικαίωμα να κάνεις kick αυτόν τον χρήστη.")
            return
        await ctx.reply(f"✅ Ο/Η {member.mention} έγινε kicked.")
        await logutil.log(
            ctx.guild, "kick",
            title=f"{emoji('logs', 'kick') or '👢'} Member Kicked",
            color=0xED4245,
            fields=[
                ("User", f"{member.mention} (`{member.id}`)", False),
                ("Λόγος", reason, False),
                ("Από", ctx.author.mention, True),
            ],
            thumbnail_url=member.display_avatar.url,
        )

    # ── DM All (CEO μόνο) ────────────────────────────────────────────────────

    @commands.command(name="dmall")
    @ceo_only()
    async def dmall_cmd(self, ctx: commands.Context, *, message: str):
        await ctx.reply(f"📨 Ξεκινάει η αποστολή DM σε {ctx.guild.member_count} μέλη")
        sent, failed = 0, 0
        for member in ctx.guild.members:
            if member.bot:
                continue
            try:
                await member.send(message)
                sent += 1
            except discord.Forbidden:
                failed += 1
            await asyncio.sleep(1)  # rate-limit friendly

        await ctx.reply(f"✅ Ολοκληρώθηκε. Στάλθηκαν: {sent} | Απέτυχαν: {failed}")
        await logutil.log(
            ctx.guild, "mod",
            title=f"{emoji('mod', 'dm') or '📨'} DM All",
            color=0x5865F2,
            fields=[
                ("Από", ctx.author.mention, True),
                ("Στάλθηκαν", str(sent), True),
                ("Απέτυχαν", str(failed), True),
                ("Μήνυμα", message[:500], False),
            ],
        )

    # ── Say / Say2 (panel με thumbnail) ──────────────────────────────────────

    @commands.command(name="say")
    @mod_only()
    async def say_cmd(self, ctx: commands.Context, channel: discord.TextChannel, *, message: str):
        container = ui.Container(accent_colour=discord.Colour.blurple())
        thumb = ctx.guild.icon.url if ctx.guild.icon else None
        if thumb:
            section = ui.Section(accessory=ui.Thumbnail(media=thumb))
            section.add_item(ui.TextDisplay(message))
            container.add_item(section)
        else:
            container.add_item(ui.TextDisplay(message))

        view = ui.LayoutView(timeout=None)
        view.add_item(container)
        try:
            await channel.send(view=view)
        except discord.HTTPException:
            await ctx.reply("⚠️ Δεν μπόρεσα να στείλω το μήνυμα σε αυτό το channel.")
            return

        await ctx.message.delete()
        await logutil.log(
            ctx.guild, "mod",
            title=f"{emoji('mod', 'say') or '📢'} Say Used",
            color=0x5865F2,
            fields=[
                ("Από", ctx.author.mention, True),
                ("Channel", channel.mention, True),
                ("Μήνυμα", message[:500], False),
            ],
        )

    @commands.command(name="say2")
    @mod_only()
    async def say2_cmd(self, ctx: commands.Context, channel: discord.TextChannel, *, payload: str):
        if "|" not in payload:
            await ctx.reply("⚠️ Χρήση: `!say2 #channel Τίτλος | Μήνυμα`")
            return
        title, message = (p.strip() for p in payload.split("|", 1))

        container = ui.Container(accent_colour=discord.Colour.blurple())
        thumb = ctx.guild.icon.url if ctx.guild.icon else None
        text = f"## {title}\n{message}"
        if thumb:
            section = ui.Section(accessory=ui.Thumbnail(media=thumb))
            section.add_item(ui.TextDisplay(text))
            container.add_item(section)
        else:
            container.add_item(ui.TextDisplay(text))

        view = ui.LayoutView(timeout=None)
        view.add_item(container)
        try:
            await channel.send(view=view)
        except discord.HTTPException:
            await ctx.reply("⚠️ Δεν μπόρεσα να στείλω το μήνυμα σε αυτό το channel.")
            return

        await ctx.message.delete()
        await logutil.log(
            ctx.guild, "mod",
            title=f"{emoji('mod', 'say') or '📢'} Say2 Used",
            color=0x5865F2,
            fields=[
                ("Από", ctx.author.mention, True),
                ("Channel", channel.mention, True),
                ("Τίτλος", title, False),
                ("Μήνυμα", message[:500], False),
            ],
        )

    # ── Error handling (καλύπτει όλες τις εντολές αυτού του cog) ────────────

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if ctx.command is None or ctx.cog is not self:
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.reply("⛔ Δεν έχεις δικαίωμα να χρησιμοποιήσεις αυτή την εντολή.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply("⚠️ Δεν βρέθηκε αυτό το μέλος.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"⚠️ Λείπει παράμετρος: `{error.param.name}`")
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.reply("⚠️ Δεν βρέθηκε αυτό το channel.")
        else:
            await ctx.reply(f"⚠️ Σφάλμα: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
