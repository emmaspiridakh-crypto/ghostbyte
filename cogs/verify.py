"""
cogs/verify.py
---------------
Verify Panel σε Components V2 με banner + κουμπί "Verify".
- Πατάς Verify -> παίρνεις τον VERIFY_ROLE_ID.
- Αν τον έχεις ήδη -> ephemeral μήνυμα, ΔΕΝ ξαναγίνεται τίποτα (δεν μπορείς
  να το "ξαναπατήσεις" ουσιαστικά, καθώς δεν σου κάνει τίποτα δεύτερη φορά).

Setup: /verify-panel (μόνο Ownership) στέλνει το panel στο τρέχον channel.
Λειτουργεί μόνιμα μέσω global on_interaction listener -> επιβιώνει σε restart.
"""

from __future__ import annotations

import discord
from discord import ui, app_commands
from discord.ext import commands

import config
from emojis import emoji
from utils import logs as logutil

VERIFY_CUSTOM_ID = "verify_btn"


def build_verify_panel() -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.blue())

    if config.VERIFY_BANNER_URL:
        container.add_item(ui.MediaGallery(discord.MediaGalleryItem(media=config.VERIFY_BANNER_URL)))

    container.add_item(ui.TextDisplay(
        f"## {emoji('verify', 'verify')} Verification\n"
        f"Πάτησε το κουμπί **Verify** παρακάτω για να αποκτήσεις πρόσβαση στον server.\n"
        f"Αν είσαι ήδη verified, δεν χρειάζεται να κάνεις κάτι άλλο."
    ))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

    btn = ui.Button(
        label="Verify",
        style=discord.ButtonStyle.success,
        emoji=emoji("verify", "verify") or "✅",
        custom_id=VERIFY_CUSTOM_ID,
    )
    row = ui.ActionRow()
    row.add_item(btn)
    container.add_item(row)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


class Verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="verify-panel", description="Στέλνει το verify panel σε αυτό το channel")
    @app_commands.checks.has_any_role(config.OWNERSHIP_ROLE_ID)
    async def verify_panel(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=build_verify_panel())

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return
        custom_id = interaction.data.get("custom_id", "")
        if custom_id != VERIFY_CUSTOM_ID:
            return

        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(config.VERIFY_ROLE_ID)

        if role is None:
            await interaction.response.send_message(
                "⚠️ Ο verify ρόλος δεν έχει ρυθμιστεί ακόμα, ενημέρωσε το staff.", ephemeral=True
            )
            return

        if role in member.roles:
            await interaction.response.send_message(
                f"{emoji('verify', 'already') or 'ℹ️'} Είσαι ήδη verified!", ephemeral=True
            )
            return

        try:
            await member.add_roles(role, reason="Verify panel")
        except discord.Forbidden:
            await interaction.response.send_message(
                "⚠️ Δεν έχω δικαίωμα να σου δώσω τον ρόλο, ενημέρωσε το staff.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"{emoji('verify', 'verified') or '✅'} Έγινες verified! Καλώς ήρθες.", ephemeral=True
        )

        await logutil.log(
            guild, "role",
            title=f"{emoji('verify', 'verify') or '✅'} Member Verified",
            color=0x57F287,
            fields=[
                ("User", f"{member.mention} (`{member.id}`)", False),
                ("Role", role.mention, True),
            ],
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Verify(bot))
