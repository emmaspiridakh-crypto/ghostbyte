"""
cogs/suggestions.py
---------------------
Suggestion Σύστημα: γράφεις μήνυμα στο SUGGESTION_CHANNEL_ID, το bot σβήνει το
αρχικό μήνυμα και το μετατρέπει αυτόματα σε panel (Components V2) με:
  - το όνομα του user (mention)
  - το κείμενο του suggestion
  - αριθμό suggestion (#N)
  - 2 κουμπιά: -1 / +1 (μετράει votes, ένας ψήφος ανά χρήστη, αλλάζει αν
    ξαναπατήσεις διαφορετικό κουμπί)
"""

from __future__ import annotations

import datetime

import discord
from discord import ui
from discord.ext import commands

import config
from emojis import emoji
from utils import db

UPVOTE_ID = "sugg_up"
DOWNVOTE_ID = "sugg_down"


def build_suggestion_view(suggestion_id: int, author_mention: str, content: str, up: int, down: int) -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.blurple())
    container.add_item(ui.TextDisplay(
        f"## {emoji('suggestion', 'suggestion') or '💡'} Suggestion #{suggestion_id}\n"
        f"**Από:** {author_mention}\n\n{content}"
    ))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

    up_btn = ui.Button(label=str(up), style=discord.ButtonStyle.success,
                        emoji=emoji("suggestion", "upvote") or "👍", custom_id=f"{UPVOTE_ID}:{suggestion_id}")
    down_btn = ui.Button(label=str(down), style=discord.ButtonStyle.danger,
                          emoji=emoji("suggestion", "downvote") or "👎", custom_id=f"{DOWNVOTE_ID}:{suggestion_id}")
    row = ui.ActionRow()
    row.add_item(up_btn)
    row.add_item(down_btn)
    container.add_item(row)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


class Suggestions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        await db.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                message_id INTEGER,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS suggestion_votes (
                suggestion_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                vote INTEGER NOT NULL,
                PRIMARY KEY (suggestion_id, user_id)
            )
        """)

    async def cog_unload(self):
        pass

    async def _get_counts(self, suggestion_id: int) -> tuple[int, int]:
        rows = await db.fetch_all(
            "SELECT vote, COUNT(*) as c FROM suggestion_votes WHERE suggestion_id = ? GROUP BY vote",
            [suggestion_id],
        )
        up = next((r["c"] for r in rows if r["vote"] == 1), 0)
        down = next((r["c"] for r in rows if r["vote"] == -1), 0)
        return up, down

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return
        if message.channel.id != config.SUGGESTION_CHANNEL_ID:
            return
        if not message.content.strip():
            return

        content = message.content
        try:
            await message.delete()
        except discord.HTTPException:
            pass

        now = datetime.datetime.now(datetime.timezone.utc).timestamp()
        rs = await db.execute(
            "INSERT INTO suggestions (guild_id, user_id, content, created_at) VALUES (?, ?, ?, ?)",
            [message.guild.id, message.author.id, content, now],
        )
        suggestion_id = rs.last_insert_rowid

        view = build_suggestion_view(suggestion_id, message.author.mention, content, 0, 0)
        sent = await message.channel.send(view=view)
        await db.execute("UPDATE suggestions SET message_id = ? WHERE id = ?", [sent.id, suggestion_id])

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return
        custom_id: str = interaction.data.get("custom_id", "")

        if not (custom_id.startswith(f"{UPVOTE_ID}:") or custom_id.startswith(f"{DOWNVOTE_ID}:")):
            return

        is_up = custom_id.startswith(f"{UPVOTE_ID}:")
        suggestion_id = int(custom_id.split(":", 1)[1])

        row = await db.fetch_one("SELECT content, user_id FROM suggestions WHERE id = ?", [suggestion_id])
        if not row:
            await interaction.response.send_message("⚠️ Δεν βρέθηκε το suggestion.", ephemeral=True)
            return

        new_vote = 1 if is_up else -1
        existing = await db.fetch_one(
            "SELECT vote FROM suggestion_votes WHERE suggestion_id = ? AND user_id = ?",
            [suggestion_id, interaction.user.id],
        )

        if existing and existing["vote"] == new_vote:
            await db.execute(
                "DELETE FROM suggestion_votes WHERE suggestion_id = ? AND user_id = ?",
                [suggestion_id, interaction.user.id],
            )
        else:
            await db.execute(
                "INSERT INTO suggestion_votes (suggestion_id, user_id, vote) VALUES (?, ?, ?) "
                "ON CONFLICT(suggestion_id, user_id) DO UPDATE SET vote = excluded.vote",
                [suggestion_id, interaction.user.id, new_vote],
            )

        up, down = await self._get_counts(suggestion_id)
        author_mention = f"<@{row['user_id']}>"
        new_view = build_suggestion_view(suggestion_id, author_mention, row["content"], up, down)
        await interaction.response.edit_message(view=new_view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Suggestions(bot))
