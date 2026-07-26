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
GUILD_ID = 1530224287808491642  # το ID του server σου (βοηθάει σε γρήγορο sync slash commands)

# ── Ρόλοι / Staff ────────────────────────────────────────────────────────────
OWNERSHIP_ROLE_ID = 1530828899280355532          # μπορεί /giveaway create, /giveaway list, delete
MANAGER_ROLE_ID = 1530828899280355532            # μπορεί /giveaway create
CEO_ROLE_ID = 1530230296023142421                # ban/unban/timeout/untimeout/kick/dmall/say/say2, partnership+buy tickets
COCEO_ROLE_ID = 1530230318626377860              # ίδια δικαιώματα με CEO
STAFF_TEAM_ROLE_IDS = [1530828899280355532]      # γενικό staff -> βλέπει owner/contact/support/seller tickets, μπορεί close/ping ticket
MOD_ROLE_IDS = [CEO_ROLE_ID, COCEO_ROLE_ID]  # roles που μπορούν τα mod commands

# ── Verify Σύστημα ───────────────────────────────────────────────────────────
VERIFY_ROLE_ID = 1530829249802534932             # ο ρόλος που παίρνεις όταν πατήσεις Verify
VERIFY_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"

# ── Ticket Σύστημα ───────────────────────────────────────────────────────────
TICKET_LANG_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"
TICKET_PANEL_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"
TICKET_PANEL_THUMBNAIL_URL = "https://i.imgur.com/Y6XXMtS.png"
TICKET_CHANNEL_THUMBNAIL_URL = "https://i.imgur.com/Y6XXMtS.png"

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
        "desc_el": "Αγορά προϊόντος", "desc_en": "I want to buy something",
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
WELCOME_CHANNEL_ID = 1530227967228121379
WELCOME_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"

# ── Reviews ──────────────────────────────────────────────────────────────────
REVIEW_PANEL_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"
REVIEW_OUTPUT_CHANNEL_ID = 1530230326310211686   # πού στέλνονται τα reviews

# ── Suggestions ──────────────────────────────────────────────────────────────
SUGGESTION_CHANNEL_ID = 1530231376002158774      # γράφεις εδώ -> γίνεται panel αυτόματα

# ── Giveaways (από το υπάρχον cog) ───────────────────────────────────────────
GIVEAWAY_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"

# ── Logs (ΞΕΧΩΡΙΣΤΟ channel για κάθε κατηγορία) ──────────────────────────────
LOG_CHANNELS = {
    "voice": 1530587880521470144,
    "channel": 1530587926591705178,
    "message": 1530587901229011095,
    "role": 1530587945122140230,
    "ticket": 1530587965238153238,
    "ban": 1530588000965103798,
    "unban": 1530588000965103798,
    "timeout": 1530588093323935994,
    "untimeout": 1530588093323935994,
    "kick": 1530588021299216457,
    "mod": 1530588115092115466,        # dmall / say / say2
    "giveaway": 1530588212307689543,
}
# Backwards-compat για το cogs/giveaways.py που ήδη έχεις (χρησιμοποιεί αυτό το όνομα)
LOG_GIVEAWAY_CHANNEL_ID = LOG_CHANNELS["giveaway"]

LOG_THUMBNAIL_URL = "https://i.imgur.com/Y6XXMtS.png"  # χρησιμοποιείται όταν δεν υπάρχει πιο συγκεκριμένο thumbnail

# ── Auto Role (δίνεται αυτόματα σε ΚΑΘΕ νέο member, χωρίς κουμπί) ───────────
AUTO_ROLE_IDS = [1530230523769782395]  # βάλε εδώ τα role IDs που θες να παίρνει αυτόματα κάθε νέο μέλος

# ── Terms of Service Panel ───────────────────────────────────────────────────
SHOP_NAME = "GhostByte"
TOS_BANNER_URL = "https://i.imgur.com/YSKTluU.jpeg"

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
