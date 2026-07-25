"""
cogs/tos.py
------------
Terms of Service panel σε Components V2, ίδιο στυλ με το reference screenshot:
  - Banner
  - Τίτλος "{SHOP_NAME} | Terms of Service"
  - Section 1: "Όροι Χρήσης (TOS)" + κουμπί "Terms Of Service"
  - Section 2: "Exchange TOS" + κουμπί "Exchange TOS"
  Κάθε κουμπί ανοίγει ephemeral μήνυμα με το αντίστοιχο κείμενο σε
  Ελληνικά + Αγγλικά (επεξεργάσιμο στο config.py).
"""

from __future__ import annotations

import discord
from discord import ui, app_commands
from discord.ext import commands

import config
from emojis import emoji

TOS_BTN_ID = "tos_view:tos"
EXCHANGE_BTN_ID = "tos_view:exchange"


def build_tos_panel() -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.orange())

    if config.TOS_BANNER_URL:
        container.add_item(ui.MediaGallery(discord.MediaGalleryItem(media=config.TOS_BANNER_URL)))

    container.add_item(ui.TextDisplay(f"**{config.SHOP_NAME} Shop | Terms of Service**"))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))

    tos_section = ui.Section(
        accessory=ui.Button(
            label="Terms Of Service",
            style=discord.ButtonStyle.secondary,
            emoji=emoji("ticket", "category") or "📋",
            custom_id=TOS_BTN_ID,
        )
    )
    tos_section.add_item(ui.TextDisplay(
        "**📋 Όροι Χρήσης (TOS)**\n"
        "• Πατήστε το παρακάτω κουμπί για να διαβάσετε τα ToS."
    ))
    container.add_item(tos_section)

    exchange_section = ui.Section(
        accessory=ui.Button(
            label="Exchange TOS",
            style=discord.ButtonStyle.secondary,
            emoji="🔄",
            custom_id=EXCHANGE_BTN_ID,
        )
    )
    exchange_section.add_item(ui.TextDisplay(
        "**🔄 Exchange TOS**\n"
        "• Πατήστε το παρακάτω κουμπί για να διαβάσετε τα Exchange ToS."
    ))
    container.add_item(exchange_section)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


def build_text_view(text_el: str, text_en: str) -> ui.LayoutView:
    container = ui.Container(accent_colour=discord.Colour.orange())
    container.add_item(ui.TextDisplay(text_el))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.small))
    container.add_item(ui.TextDisplay(text_en))
    view = ui.LayoutView(timeout=None)
    view.add_item(container)
    return view


class TermsOfService(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="tos-panel", description="Στέλνει το Terms of Service panel σε αυτό το channel")
    @app_commands.checks.has_any_role(config.OWNERSHIP_ROLE_ID)
    async def tos_panel(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=build_tos_panel())

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return
        custom_id: str = interaction.data.get("custom_id", "")

        if custom_id == TOS_BTN_ID:
            view = build_text_view(config.TOS_TEXT_EL, config.TOS_TEXT_EN)
            await interaction.response.send_message(view=view, ephemeral=True)
        elif custom_id == EXCHANGE_BTN_ID:
            view = build_text_view(config.EXCHANGE_TOS_TEXT_EL, config.EXCHANGE_TOS_TEXT_EN)
            await interaction.response.send_message(view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(TermsOfService(bot))
