"""
cogs/tickets.py
-----------------
Ticket Σύστημα σε Components V2, με SQLite persistence.

Ροή:
  /ticket-panel  (Ownership)  → στέλνει "Language Panel" (banner) με 2 κουμπιά:
                                 🇬🇷 Ελληνικά | 🇬🇧 English
  Πατάς γλώσσα                → ephemeral panel (banner + thumbnail + dropdown
                                 με τα categories) στην επιλεγμένη γλώσσα
  Επιλέγεις category           → δημιουργείται ticket channel στην αντίστοιχη
                                 Discord category, με permissions μόνο για τον
                                 opener + τους viewer roles του τύπου.
                                 Μέσα στο channel: panel (thumbnail) με το
                                 όνομα + τον τύπο ticket, και 2 κουμπιά:
                                 🔒 Close Ticket | 🔔 Ping User
                                 (μόνο staff μπορεί να τα πατήσει, όχι ο opener)

Persistence: όλα τα tickets αποθηκεύονται σε SQLite, άρα το bot δεν χάνει
τίποτα σε restart. Τα buttons λειτουργούν μέσω global on_interaction listener
(δεν χρειάζεται re-register persistent view per-message).
"""

from __future__ import annotations

import datetime
from typing import Optional

import discord
from discord import ui, app_commands
from discord.ext import commands

import config
from emojis import emoji
from utils.permissions import has_roles
from utils import logs as logutil
from utils import db

TEXT = {
    "el": {
        "panel_title": "🎫 Άνοιγμα Ticket",
        "panel_desc": "Διάλεξε από το μενού παρακάτω τον λόγο που ανοίγεις ticket.",
        "placeholder": "Διάλεξε κατηγορία...",
        "created": "✅ Το ticket σου δημιουργήθηκε: {mention}",
        "already_open": "⚠️ Έχεις ήδη ανοιχτό ticket αυτού του τύπου: {mention}",
        "channel_intro": "## {emoji} Ticket — {type_label}\n**Άνοιξε από:** {user}\n\nΈνα μέλος του staff θα σε εξυπηρετήσει σύντομα. Περίγραψε το θέμα σου.",
    },
    "en": {
        "panel_title": "🎫 Open a Ticket",
        "panel_desc": "Pick the reason you're opening a ticket from the menu below.",
        "placeholder": "Select a category...",
        "created": "✅ Your ticket has been created: {mention}",
        "already_open": "⚠️ You already have an open ticket of this type: {mention}",
        "channel_intro": "## {emoji} Ticket — {type_label}\n**Opened by:** {user}\n\nA staff member will assist you shortly. Please describe your issue.",
    },
}

LANG_CUSTOM_ID = "ticket_lang"
SELECT_CUSTOM_ID = "ticket_select"
CLOSE_CUSTOM_ID = "ticket_close"
PING_CUSTOM_ID = "ticket_ping"


def _lang_label(ticket_type: dict, lang: str) -> str:
    return ticket_type[f"label_{lang}"]


def build_lang_panel() -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.blue())
    if config.TICKET_LANG_BANNER_URL:
        container.add_item(ui.MediaGallery(discord.MediaGalleryItem(media=config.TICKET_LANG_BANNER_URL)))
    container.add_item(ui.TextDisplay(
        f"## {emoji('ticket', 'ticket') or '🎫'} Support Tickets\n"
        f"Επίλεξε γλώσσα / Select your language"
    ))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

    el_btn = ui.Button(label="Ελληνικά", style=discord.ButtonStyle.secondary,
                        emoji=emoji("ticket", "greek") or "🇬🇷", custom_id=f"{LANG_CUSTOM_ID}:el")
    en_btn = ui.Button(label="English", style=discord.ButtonStyle.secondary,
                        emoji=emoji("ticket", "english") or "🇬🇧", custom_id=f"{LANG_CUSTOM_ID}:en")
    row = ui.ActionRow()
    row.add_item(el_btn)
    row.add_item(en_btn)
    container.add_item(row)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


def build_category_panel(lang: str) -> ui.LayoutView:
    t = TEXT[lang]
    container = ui.Container(accent_colour=discord.Colour.blue())

    if config.TICKET_PANEL_BANNER_URL:
        container.add_item(ui.MediaGallery(discord.MediaGalleryItem(media=config.TICKET_PANEL_BANNER_URL)))

    section = ui.Section(accessory=ui.Thumbnail(media=config.TICKET_PANEL_THUMBNAIL_URL)) if config.TICKET_PANEL_THUMBNAIL_URL else None
    text = f"## {t['panel_title']}\n{t['panel_desc']}"
    if section:
        section.add_item(ui.TextDisplay(text))
        container.add_item(section)
    else:
        container.add_item(ui.TextDisplay(text))

    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

    select = ui.Select(
        placeholder=t["placeholder"],
        custom_id=f"{SELECT_CUSTOM_ID}:{lang}",
        options=[
            discord.SelectOption(
                label=_lang_label(ttype, lang),
                description=ttype[f"desc_{lang}"][:100],
                value=key,
                emoji=ttype.get("emoji"),
            )
            for key, ttype in config.TICKET_TYPES.items()
        ],
    )
    row = ui.ActionRow()
    row.add_item(select)
    container.add_item(row)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


def build_channel_panel(lang: str, ticket_id: int, ttype_key: str, opener: discord.Member) -> ui.LayoutView:
    t = TEXT[lang]
    ttype = config.TICKET_TYPES[ttype_key]
    label = _lang_label(ttype, lang)

    container = ui.Container(accent_colour=discord.Colour.gold())

    text = t["channel_intro"].format(emoji=ttype.get("emoji", "🎫"), type_label=label, user=opener.mention)
    if config.TICKET_CHANNEL_THUMBNAIL_URL:
        section = ui.Section(accessory=ui.Thumbnail(media=config.TICKET_CHANNEL_THUMBNAIL_URL))
        section.add_item(ui.TextDisplay(text))
        container.add_item(section)
    else:
        container.add_item(ui.TextDisplay(text))

    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

    close_btn = ui.Button(label="Close Ticket", style=discord.ButtonStyle.danger,
                           emoji=emoji("ticket", "close") or "🔒", custom_id=f"{CLOSE_CUSTOM_ID}:{ticket_id}")
    ping_btn = ui.Button(label="Ping User", style=discord.ButtonStyle.secondary,
                          emoji=emoji("ticket", "ping") or "🔔", custom_id=f"{PING_CUSTOM_ID}:{ticket_id}")
    row = ui.ActionRow()
    row.add_item(close_btn)
    row.add_item(ping_btn)
    container.add_item(row)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                ticket_type TEXT NOT NULL,
                lang TEXT NOT NULL DEFAULT 'el',
                status TEXT NOT NULL DEFAULT 'open',
                created_at REAL NOT NULL,
                closed_at REAL
            )
        """)

    async def cog_unload(self):
        pass

    # ── DB helpers ────────────────────────────────────────────────────────────

    async def db_get(self, ticket_id: int) -> Optional[dict]:
        return await db.fetch_one("SELECT * FROM tickets WHERE id = ?", [ticket_id])

    async def db_get_open_by_user(self, guild_id: int, user_id: int, ticket_type: str) -> Optional[dict]:
        return await db.fetch_one(
            "SELECT * FROM tickets WHERE guild_id = ? AND user_id = ? AND ticket_type = ? AND status = 'open'",
            [guild_id, user_id, ticket_type],
        )

    async def db_create(self, guild_id: int, channel_id: int, user_id: int, ticket_type: str, lang: str) -> int:
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        rs = await db.execute(
            "INSERT INTO tickets (guild_id, channel_id, user_id, ticket_type, lang, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, 'open', ?)",
            [guild_id, channel_id, user_id, ticket_type, lang, now],
        )
        return rs.last_insert_rowid

    async def db_close(self, ticket_id: int):
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        await db.execute("UPDATE tickets SET status = 'closed', closed_at = ? WHERE id = ?", [now, ticket_id])

    # ── Slash command ────────────────────────────────────────────────────────

    @app_commands.command(name="ticket-panel", description="Στέλνει το ticket language panel σε αυτό το channel")
    @app_commands.checks.has_any_role(config.OWNERSHIP_ROLE_ID)
    async def ticket_panel(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=build_lang_panel())

    # ── Interaction listener ─────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return
        custom_id: str = interaction.data.get("custom_id", "")

        if custom_id.startswith(f"{LANG_CUSTOM_ID}:"):
            lang = custom_id.split(":", 1)[1]
            await interaction.response.send_message(view=build_category_panel(lang), ephemeral=True)
        elif custom_id.startswith(f"{CLOSE_CUSTOM_ID}:"):
            await self._handle_close(interaction, int(custom_id.split(":", 1)[1]))
        elif custom_id.startswith(f"{PING_CUSTOM_ID}:"):
            await self._handle_ping(interaction, int(custom_id.split(":", 1)[1]))
        elif custom_id.startswith(f"{SELECT_CUSTOM_ID}:"):
            lang = custom_id.split(":", 1)[1]
            ttype_key = interaction.data.get("values", [None])[0]
            if ttype_key not in config.TICKET_TYPES:
                return
            await self._handle_create_ticket(interaction, lang, ttype_key)

    # ── Handlers ──────────────────────────────────────────────────────────────

    async def _handle_create_ticket(self, interaction: discord.Interaction, lang: str, ttype_key: str):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        user = interaction.user
        t = TEXT[lang]
        ttype = config.TICKET_TYPES[ttype_key]

        existing = await self.db_get_open_by_user(guild.id, user.id, ttype_key)
        if existing:
            ch = guild.get_channel(existing["channel_id"])
            if ch:
                await interaction.followup.send(t["already_open"].format(mention=ch.mention), ephemeral=True)
                return

        category = guild.get_channel(ttype["category_id"]) if ttype["category_id"] else None

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }
        for rid in ttype["viewer_role_ids"]:
            role = guild.get_role(rid)
            if role:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        safe_name = "".join(c for c in user.name.lower() if c.isalnum()) or "user"
        channel_name = f"{ttype_key}-{safe_name}"[:90]

        try:
            channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites,
                reason=f"Ticket ({ttype_key}) από {user}",
            )
        except discord.Forbidden:
            await interaction.followup.send("⚠️ Δεν έχω δικαίωμα να δημιουργήσω το ticket channel.", ephemeral=True)
            return

        ticket_id = await self.db_create(guild.id, channel.id, user.id, ttype_key, lang)

        panel = build_channel_panel(lang, ticket_id, ttype_key, user)
        try:
            await channel.send(content=user.mention, view=panel, allowed_mentions=discord.AllowedMentions(users=True))
        except discord.HTTPException:
            pass

        await interaction.followup.send(t["created"].format(mention=channel.mention), ephemeral=True)

        await logutil.log(
            guild, "ticket",
            title=f"{emoji('logs', 'ticket') or '🎫'} Ticket Opened",
            color=0x57F287,
            fields=[
                ("ID", f"`#{ticket_id}`", True),
                ("Type", _lang_label(ttype, lang), True),
                ("User", f"{user.mention} (`{user.id}`)", False),
                ("Channel", channel.mention, True),
            ],
        )

    async def _handle_close(self, interaction: discord.Interaction, ticket_id: int):
        ticket = await self.db_get(ticket_id)
        if not ticket or ticket["status"] != "open":
            await interaction.response.send_message("⚠️ Αυτό το ticket δεν είναι πλέον ανοιχτό.", ephemeral=True)
            return

        ttype = config.TICKET_TYPES.get(ticket["ticket_type"])
        member = interaction.user
        if member.id == ticket["user_id"] or not has_roles(member, ttype["viewer_role_ids"] if ttype else []):
            await interaction.response.send_message(
                "⛔ Μόνο μέλος του staff μπορεί να κλείσει αυτό το ticket (όχι ο χρήστης που το άνοιξε).",
                ephemeral=True,
            )
            return

        await interaction.response.send_message("🔒 Το ticket κλείνει σε 5 δευτερόλεπτα...")
        await self.db_close(ticket_id)

        guild = interaction.guild
        opener = guild.get_member(ticket["user_id"])
        if opener:
            try:
                await opener.send(f"🔒 Το ticket σου (`#{ticket_id}`) στο **{guild.name}** έκλεισε από {member.mention}.")
            except discord.Forbidden:
                pass

        await logutil.log(
            guild, "ticket",
            title=f"{emoji('ticket', 'close') or '🔒'} Ticket Closed",
            color=0xED4245,
            fields=[
                ("ID", f"`#{ticket_id}`", True),
                ("Type", ticket["ticket_type"], True),
                ("Opened by", f"<@{ticket['user_id']}>", True),
                ("Closed by", member.mention, True),
            ],
        )

        channel = guild.get_channel(ticket["channel_id"])
        if channel:
            import asyncio
            await asyncio.sleep(5)
            try:
                await channel.delete(reason=f"Ticket closed by {member}")
            except discord.HTTPException:
                pass

    async def _handle_ping(self, interaction: discord.Interaction, ticket_id: int):
        ticket = await self.db_get(ticket_id)
        if not ticket or ticket["status"] != "open":
            await interaction.response.send_message("⚠️ Αυτό το ticket δεν είναι πλέον ανοιχτό.", ephemeral=True)
            return

        ttype = config.TICKET_TYPES.get(ticket["ticket_type"])
        member = interaction.user
        if member.id == ticket["user_id"] or not has_roles(member, ttype["viewer_role_ids"] if ttype else []):
            await interaction.response.send_message(
                "⛔ Μόνο μέλος του staff μπορεί να κάνει ping εδώ.", ephemeral=True
            )
            return

        guild = interaction.guild
        opener = guild.get_member(ticket["user_id"])
        mention = opener.mention if opener else f"<@{ticket['user_id']}>"

        await interaction.response.send_message(
            f"🔔 {mention}, το staff περιμένει την απάντησή σου σε αυτό το ticket.",
            allowed_mentions=discord.AllowedMentions(users=True),
        )

        if opener:
            try:
                await opener.send(
                    f"🔔 Έχεις ping από το staff στο ticket `#{ticket_id}` στο **{guild.name}**. "
                    f"Πήγαινε στο channel για να απαντήσεις."
                )
            except discord.Forbidden:
                pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
