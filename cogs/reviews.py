"""
cogs/reviews.py
-----------------
Review Σύστημα σε Components V2.

Ροή:
  /review-panel (Ownership)  → στέλνει panel (banner) με κουμπί "Submit a review"
  Πατάς το κουμπί            → ephemeral Select (1-5 αστέρια)
  Επιλέγεις αστέρια           → Modal για σχόλιο
  Submit                      → review στέλνεται σε REVIEW_OUTPUT_CHANNEL_ID:
                                 thumbnail, αστέρια, ποιος το έκανε (mention),
                                 σχόλιο, αριθμός review (#N)
"""

from __future__ import annotations

import datetime

import discord
from discord import ui, app_commands
from discord.ext import commands

import config
from emojis import emoji
from utils import db

SUBMIT_BTN_ID = "review_submit"
STAR_SELECT_ID = "review_stars"


def build_review_panel() -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.blue())
    if config.REVIEW_PANEL_BANNER_URL:
        container.add_item(ui.MediaGallery(discord.MediaGalleryItem(media=config.REVIEW_PANEL_BANNER_URL)))
    container.add_item(ui.TextDisplay(
        f"## {emoji('review', 'review') or '⭐'} Άφησε μια αξιολόγηση\n"
        f"Μας ενδιαφέρει η γνώμη σου! Πάτησε το κουμπί παρακάτω για να αφήσεις review."
    ))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))
    btn = ui.Button(label="Submit a review", style=discord.ButtonStyle.primary,
                     emoji=emoji("review", "submit") or "📝", custom_id=SUBMIT_BTN_ID)
    row = ui.ActionRow()
    row.add_item(btn)
    container.add_item(row)
    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


def build_star_select_view() -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.blue())
    container.add_item(ui.TextDisplay(f"## {emoji('review', 'star') or '⭐'} Πόσα αστέρια θα έδινες;"))
    select = ui.Select(
        placeholder="Επίλεξε βαθμολογία (1-5)",
        custom_id=STAR_SELECT_ID,
        options=[
            discord.SelectOption(label=f"{i} {'⭐' * i}", value=str(i))
            for i in range(1, 6)
        ],
    )
    row = ui.ActionRow()
    row.add_item(select)
    container.add_item(row)
    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


class ReviewCommentModal(ui.Modal, title="Το σχόλιό σου"):
    comment = ui.TextInput(label="Σχόλιο", style=discord.TextStyle.paragraph, max_length=1000, required=True)

    def __init__(self, cog: "Reviews", stars: int):
        super().__init__()
        self.cog = cog
        self.stars = stars

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.cog.post_review(interaction, self.stars, str(self.comment))
        await interaction.followup.send("✅ Ευχαριστούμε για το review σου!", ephemeral=True)


class Reviews(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                stars INTEGER NOT NULL,
                comment TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)

    async def cog_unload(self):
        pass

    async def post_review(self, interaction: discord.Interaction, stars: int, comment: str):
        guild = interaction.guild
        user = interaction.user
        now = datetime.datetime.now(datetime.timezone.utc).timestamp()

        rs = await db.execute(
            "INSERT INTO reviews (guild_id, user_id, stars, comment, created_at) VALUES (?, ?, ?, ?, ?)",
            [guild.id, user.id, stars, comment, now],
        )
        review_number = rs.last_insert_rowid

        channel = guild.get_channel(config.REVIEW_OUTPUT_CHANNEL_ID)
        if channel is None:
            return

        star_str = (emoji("review", "star") or "⭐") * stars + (emoji("review", "star_empty") or "☆") * (5 - stars)

        container = ui.Container(accent_colour=discord.Colour.gold())
        section = ui.Section(accessory=ui.Thumbnail(media=user.display_avatar.url))
        section.add_item(ui.TextDisplay(
            f"## {emoji('review', 'review') or '⭐'} Review #{review_number}\n"
            f"**Από:** {user.mention}\n"
            f"**Βαθμολογία:** {star_str} ({stars}/5)\n\n"
            f"{comment}"
        ))
        container.add_item(section)

        view = ui.LayoutView(timeout=None)
        view.add_item(container)
        try:
            await channel.send(view=view)
        except discord.HTTPException:
            pass

    @app_commands.command(name="review-panel", description="Στέλνει το review panel σε αυτό το channel")
    @app_commands.checks.has_any_role(config.OWNERSHIP_ROLE_ID)
    async def review_panel(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=build_review_panel())

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return
        custom_id: str = interaction.data.get("custom_id", "")

        if custom_id == SUBMIT_BTN_ID:
            await interaction.response.send_message(view=build_star_select_view(), ephemeral=True)
        elif custom_id == STAR_SELECT_ID:
            stars = int(interaction.data.get("values", ["5"])[0])
            await interaction.response.send_modal(ReviewCommentModal(self, stars))


async def setup(bot: commands.Bot):
    await bot.add_cog(Reviews(bot))
