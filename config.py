"""
config.py
---------
Όλες οι ρυθμίσεις του bot. ΣΥΜΠΛΗΡΩΣΕ τα IDs πριν τρέξεις το bot.
Πώς παίρνεις IDs: Discord Settings -> Advanced -> Developer Mode ON,
μετά δεξί κλικ σε server/channel/role/member -> Copy ID.
"""

import os

# ── Bot ──────────────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
PREFIX = "!"
GUILD_ID = 0  # το ID του server σου (βοηθάει σε γρήγορο sync slash commands)

# ── Ρόλοι / Staff ────────────────────────────────────────────────────────────
OWNERSHIP_ROLE_ID = 0          # μπορεί /giveaway create, /giveaway list, delete
MANAGER_ROLE_ID = 0            # μπορεί /giveaway create
CEO_ROLE_ID = 0                # ban/unban/timeout/untimeout/kick/dmall/say/say2, partnership+buy tickets
COCEO_ROLE_ID = 0              # ίδια δικαιώματα με CEO
STAFF_TEAM_ROLE_IDS = [0]      # γενικό staff -> βλέπει owner/contact/support/seller tickets, μπορεί close/ping ticket
MOD_ROLE_IDS = [CEO_ROLE_ID, COCEO_ROLE_ID]  # roles που μπορούν τα mod commands

# ── Verify Σύστημα ───────────────────────────────────────────────────────────
VERIFY_ROLE_ID = 0             # ο ρόλος που παίρνεις όταν πατήσεις Verify
VERIFY_BANNER_URL = "https://example.com/verify_banner.png"

# ── Ticket Σύστημα ───────────────────────────────────────────────────────────
TICKET_LANG_BANNER_URL = "https://example.com/ticket_lang_banner.png"
TICKET_PANEL_BANNER_URL = "https://example.com/ticket_panel_banner.png"
TICKET_PANEL_THUMBNAIL_URL = "https://example.com/ticket_panel_thumbnail.png"
TICKET_CHANNEL_THUMBNAIL_URL = "https://example.com/ticket_channel_thumbnail.png"

# Κάθε τύπος ticket: ξεχωριστό Discord Category (channel category), και ποιοι ρόλοι το βλέπουν.
# category_id = 0 -> ΠΡΕΠΕΙ να το γεμίσεις με το ID της discord category που θα φιλοξενεί τα tickets αυτού του τύπου.
TICKET_TYPES = {
    "owner": {
        "label_el": "Owner", "label_en": "Owner",
        "desc_el": "Επικοινωνία με τον owner", "desc_en": "Contact the owner",
        "emoji": "👑",
        "category_id": 0,
        "viewer_role_ids": STAFF_TEAM_ROLE_IDS,
    },
    "contact_support": {
        "label_el": "Επικοινωνία / Support", "label_en": "Contact / Support",
        "desc_el": "Γενική βοήθεια & ερωτήσεις", "desc_en": "General help & questions",
        "emoji": "🛠️",
        "category_id": 0,
        "viewer_role_ids": STAFF_TEAM_ROLE_IDS,
    },
    "partnership": {
        "label_el": "Partnership", "label_en": "Partnership",
        "desc_el": "Προτάσεις συνεργασίας", "desc_en": "Partnership proposals",
        "emoji": "🤝",
        "category_id": 0,
        "viewer_role_ids": [CEO_ROLE_ID, COCEO_ROLE_ID],
    },
    "buy": {
        "label_el": "Αγορά", "label_en": "Buy",
        "desc_el": "Θέλω να αγοράσω κάτι", "desc_en": "I want to buy something",
        "emoji": "🛒",
        "category_id": 0,
        "viewer_role_ids": [CEO_ROLE_ID, COCEO_ROLE_ID],
    },
    "seller": {
        "label_el": "Seller", "label_en": "Seller",
        "desc_el": "Θέμα σχετικό με πωλητή", "desc_en": "Seller related matter",
        "emoji": "💼",
        "category_id": 0,
        "viewer_role_ids": STAFF_TEAM_ROLE_IDS,
    },
}

# ── Welcome ──────────────────────────────────────────────────────────────────
WELCOME_CHANNEL_ID = 0
WELCOME_BANNER_URL = "https://example.com/welcome_banner.png"

# ── Reviews ──────────────────────────────────────────────────────────────────
REVIEW_PANEL_BANNER_URL = "https://example.com/review_banner.png"
REVIEW_OUTPUT_CHANNEL_ID = 0   # πού στέλνονται τα reviews

# ── Suggestions ──────────────────────────────────────────────────────────────
SUGGESTION_CHANNEL_ID = 0      # γράφεις εδώ -> γίνεται panel αυτόματα

# ── Giveaways (από το υπάρχον cog) ───────────────────────────────────────────
GIVEAWAY_BANNER_URL = "https://example.com/giveaway_banner.png"

# ── Logs (ΞΕΧΩΡΙΣΤΟ channel για κάθε κατηγορία) ──────────────────────────────
LOG_CHANNELS = {
    "voice": 0,
    "channel": 0,
    "message": 0,
    "role": 0,
    "ticket": 0,
    "ban": 0,
    "unban": 0,
    "timeout": 0,
    "untimeout": 0,
    "kick": 0,
    "mod": 0,        # dmall / say / say2
    "giveaway": 0,
}
# Backwards-compat για το cogs/giveaways.py που ήδη έχεις (χρησιμοποιεί αυτό το όνομα)
LOG_GIVEAWAY_CHANNEL_ID = LOG_CHANNELS["giveaway"]

LOG_THUMBNAIL_URL = "https://example.com/log_thumbnail.png"  # χρησιμοποιείται όταν δεν υπάρχει πιο συγκεκριμένο thumbnail

# ── Auto Role (δίνεται αυτόματα σε ΚΑΘΕ νέο member, χωρίς κουμπί) ───────────
AUTO_ROLE_IDS = [0]  # βάλε εδώ τα role IDs που θες να παίρνει αυτόματα κάθε νέο μέλος

# ── Terms of Service Panel ───────────────────────────────────────────────────
SHOP_NAME = "GhostByte"
TOS_BANNER_URL = "https://example.com/tos_banner.png"

TOS_TEXT_EL = (
    f"## 📋 Όροι Χρήσης — {SHOP_NAME}\n"
    "Συμπλήρωσε εδώ το πλήρες κείμενο των Terms of Service στα Ελληνικά."
)
TOS_TEXT_EN = (
    f"## 📋 Terms of Service — {SHOP_NAME}\n"
    "Fill in the full Terms of Service text in English here."
)
EXCHANGE_TOS_TEXT_EL = (
    f"## 🔄 Όροι Ανταλλαγής (Exchange TOS) — {SHOP_NAME}\n"
    "Συμπλήρωσε εδώ το πλήρες κείμενο των Exchange ToS στα Ελληνικά."
)
EXCHANGE_TOS_TEXT_EN = (
    f"## 🔄 Exchange Terms of Service — {SHOP_NAME}\n"
    "Fill in the full Exchange ToS text in English here."
)

# ── Keep-alive (Render) ──────────────────────────────────────────────────────
FLASK_PORT = int(os.getenv("PORT", 1000))
