"""
config.py
---------
Όλες οι ρυθμίσεις του bot. ΣΥΜΠΛΗΡΩΣΕ τα IDs πριν τρέξεις το bot.
Πώς παίρνεις IDs: Discord Settings -> Advanced -> Developer Mode ON,
μετά δεξί κλικ σε server/channel/role/member -> Copy ID.
"""

import os

from emojis import emoji as _emoji

# ── Bot ──────────────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
PREFIX = "!"
GUILD_ID = 1530224287808491642  # το ID του server σου (βοηθάει σε γρήγορο sync slash commands)

# ── Ρόλοι / Staff ────────────────────────────────────────────────────────────
OWNERSHIP_ROLE_ID = 1530828899280355532          # μπορεί /giveaway create, /giveaway list, delete
MANAGER_ROLE_ID = 1530828899280355532          # μπορεί /giveaway create
CEO_ROLE_ID = 1530828899280355532                # ban/unban/timeout/untimeout/kick/dmall/say/say2, partnership+buy tickets
COCEO_ROLE_ID = 1530828899280355532              # ίδια δικαιώματα με CEO
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
        "category_id": 1530588297385218126,
        "viewer_role_ids": STAFF_TEAM_ROLE_IDS,
    },
    "contact_support": {
        "label_el": "Επικοινωνία / Support", "label_en": "Contact / Support",
        "desc_el": "Γενική βοήθεια & ερωτήσεις", "desc_en": "General help & questions",
        "emoji": "🛠️",
        "category_id": 1530588440973017188,
        "viewer_role_ids": STAFF_TEAM_ROLE_IDS,
    },
    "partnership": {
        "label_el": "Partnership", "label_en": "Partnership",
        "desc_el": "Προτάσεις συνεργασίας", "desc_en": "Partnership proposals",
        "emoji": "🤝",
        "category_id": 1530588673727529160,
        "viewer_role_ids": [CEO_ROLE_ID, COCEO_ROLE_ID],
    },
    "buy": {
        "label_el": "Αγορά", "label_en": "Buy",
        "desc_el": "Αγορά προϊόντος", "desc_en": "I want to buy something",
        "emoji": "🛒",
        "category_id": 1530588363118215219,
        "viewer_role_ids": [CEO_ROLE_ID, COCEO_ROLE_ID],
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
    f"## {_emoji('tos', 'document') or '📋'} Όροι Χρήσης — {SHOP_NAME}\n\n"
    "• Οι κανόνες μπορούν να αλλάξουν ανά πάσα ώρα και στιγμή. Εσείς οι ίδιοι είστε υποχρεωμένοι να διαβάζετε τους κανόνες συστηματικά.\n\n"
    "• Οι τιμές και οι όροι μπορούν να αλλάξουν ανά πάσα στιγμή χωρίς προηγούμενη ειδοποίηση.\n\n"
    "• Διατηρούμε το δικαίωμα να αρνηθούμε την παροχή οποιασδήποτε υπηρεσίας σε οποιονδήποτε, οποτεδήποτε.\n\n"
    "• Με την πραγματοποίηση αγοράς, θεωρείται ότι έχετε διαβάσει, κατανοήσει και αποδεχτεί πλήρως τους όρους χρήσης. Η άγνοια των όρων δεν αποτελεί δικαιολογία.\n\n"
    "• Μετά την ολοκλήρωση κάθε παραγγελίας, η κατάθεση vouch στο αντίστοιχο κανάλι είναι υποχρεωτική. Σε αντίθετη περίπτωση, ενδέχεται να σας απαγορευτεί η μελλοντική χρήση των υπηρεσιών μας.\n\n"
    "• Οποιεσδήποτε κατηγορίες περί scam (απάτης) χωρίς τα απαραίτητα και ξεκάθαρα αποδεικτικά στοιχεία οδηγούν σε άμεσο και μόνιμο αποκλεισμό (Permanent Ban) από τον διακομιστή.\n\n"
    "• Αν κάποιος seller/maker/exchanger κάνει exit scam δεν θα υπάρξει refund από το ownership team εκτός αν έρθουμε σε επικοινωνία με τον seller/maker/exchanger και επιστρέψει ο ίδιος το προϊόν ή τα χρήματα.\n\n"
    "• Για κάθε αγορά που κάνετε είστε υποχρεωμένοι να έχετε κάποιο clip από όλη την συναλλαγή.\n\n"
    "• Δεν αποδεχόμαστε αγορές για τρίτους πέρα από reselling. Όμως από την στιγμή που δώσουμε το προϊόν και είναι εντάξει, από εκεί και πέρα είναι δική σας ευθύνη για ό,τι συμβεί στο προϊόν.\n\n"
    "• Οι παραπάνω κανόνες ισχύουν και για τα Exchange ToS."
)
TOS_TEXT_EN = (
    f"## {_emoji('tos', 'document') or '📋'} Terms of Service — {SHOP_NAME}\n\n"
    "• These terms may be updated at any time without notice. You are responsible for reviewing them periodically.\n\n"
    "• Prices and terms may be changed at any time without prior notice.\n\n"
    "• We reserve the right to refuse service to anyone, at any time.\n\n"
    "• By making a purchase, you acknowledge that you have read, understood, and fully accepted the Terms of Service. Ignorance of the terms does not constitute an excuse.\n\n"
    "• After the completion of every order, leaving a vouch in the designated channel is mandatory. Failure to do so may result in restrictions on your future use of our services.\n\n"
    "• Any accusations of scamming without clear and sufficient evidence will result in an immediate and permanent ban from the server.\n\n"
    "• If any seller/maker/exchanger performs an exit scam, no refund will be provided by the ownership team unless we are able to contact the seller/maker/exchanger and they personally return the product or issue a refund.\n\n"
    "• For any product that you buy, you are required to have a clip of the whole transaction.\n\n"
    "• We don't accept third party purchases, other than for reselling. As soon as we deliver the product and it's okay, from then on it's your responsibility for anything that happens to the product.\n\n"
    "• These terms also apply to the Exchange ToS."
)
EXCHANGE_TOS_TEXT_EL = (
    f"## {_emoji('tos', 'exchange') or '🔄'} Όροι Ανταλλαγής (Exchange TOS) — {SHOP_NAME}\n\n"
    "• Τα χρήματα πρέπει να σταλθούν στο σωστό email και επίσης να τσεκάρετε το email που στείλατε για να λάβετε τα χρήματα. Είστε υποχρεωμένοι να διπλό τσεκάρετε το email που σας έχει στείλει ο exchanger και το email που στείλατε.\n\n"
    "• Σε περίπτωση που στείλετε παραπάνω χρήματα ο exchanger δεν είναι αναγκασμένος να επιστρέψει το extra ποσό.\n\n"
    "**PayPal Rules**\n"
    "• Τα χρήματα πρέπει να σταλθούν Friends & Family εκτός αν έχει υπάρξει συνεννόηση με τον exchanger.\n\n"
    "• Τα χρήματα πρέπει να σταλθούν από το PayPal Balance εκτός αν έχει υπάρξει συνεννόηση με τον exchanger.\n\n"
    "• Τα λεφτά πρέπει να σταλθούν στο συνεννοημένο νόμισμα.\n\n"
    "• Η συναλλαγή πρέπει να γίνει χωρίς κάποια notes στο PayPal.\n\n"
    "**Crypto**\n"
    "• Τα χρήματα πρέπει να σταλθούν στο κρυπτονόμισμα στο οποίο έχει συνεννοηθεί με τον exchanger.\n\n"
    "• Το TXID είναι υποχρεωτικό μετά από κάθε συναλλαγή.\n\n"
    "• Τα χρήματα πρέπει να σταλθούν στο σωστό addy (wallet).\n\n"
    "**Paysafe Rules**\n"
    "• Ο κωδικός/QR της Paysafe πρέπει να σταλθεί σε προσωπικό μήνυμα (DM). Σε περίπτωση που σταλθεί σε κάποιο κανάλι στο οποίο έχουν access και άλλα άτομα, και η Paysafe χρησιμοποιηθεί από κάποιον άλλον, ο exchanger δεν είναι υποχρεωμένος να επιστρέψει κάποια χρήματα.\n\n"
    "• Οι κωδικοί της Paysafe πρέπει να είναι αχρησιμοποίητοι.\n\n"
    "**Περιορισμός Ευθύνης**\n"
    "• Ο exchanger δεν φέρει καμία ευθύνη για τυχόν απώλειες που προκύπτουν από αμέλεια ή σφάλμα του χρήστη, συμπεριλαμβανομένων ενδεικτικά αλλά όχι περιοριστικά λανθασμένων στοιχείων πληρωμής, εσφαλμένων διευθύνσεων πορτοφολιού (wallet addresses), λανθασμένου νομίσματος, μη εξουσιοδοτημένης κοινοποίησης κωδικών πληρωμής ή μη συμμόρφωσης με τους παρόντες Όρους Χρήσης.\n\n"
    "**Με την πραγματοποίηση οποιασδήποτε συναλλαγής ανταλλαγής, ο χρήστης αναγνωρίζει και αποδέχεται πλήρως όλους τους κινδύνους που σχετίζονται με τη μέθοδο πληρωμής που επιλέγει να χρησιμοποιήσει.**"
)
EXCHANGE_TOS_TEXT_EN = (
    f"## {_emoji('tos', 'exchange') or '🔄'} Exchange Terms of Service — {SHOP_NAME}\n\n"
    "• All parties are solely responsible for verifying the accuracy of the recipient's email address, wallet address, or any other payment details before initiating a transaction.\n\n"
    "• Users are required to double-check both the payment information provided by the exchanger and the payment information they submit for receiving funds.\n\n"
    "• In the event that a user sends funds in excess of the agreed amount, the exchanger shall not be obligated to refund or return any excess funds.\n\n"
    "• Once a transaction has been completed and confirmed, it shall be considered final unless otherwise agreed by both parties.\n\n"
    "**PayPal Transactions**\n"
    "• Unless explicitly agreed otherwise, all PayPal payments must be sent using the Friends & Family payment method.\n\n"
    "• Unless explicitly agreed otherwise, all PayPal payments must be funded directly from the sender's PayPal Balance.\n\n"
    "• Payments must be sent in the currency mutually agreed upon prior to the transaction.\n\n"
    "• No notes, comments, references, or descriptions may be included in the PayPal transaction unless specifically authorized by the exchanger.\n\n"
    "• Failure to comply with any PayPal-related requirements may result in delays, cancellation of the exchange, or refusal of service.\n\n"
    "**Cryptocurrency Transactions**\n"
    "• Funds must be sent exclusively in the cryptocurrency agreed upon by both parties prior to the transaction.\n\n"
    "• The sender must provide a valid Transaction ID (TXID) immediately after the transaction has been broadcast to the blockchain.\n\n"
    "• The sender is solely responsible for ensuring that funds are sent to the correct wallet address.\n\n"
    "• Cryptocurrency transactions are irreversible. Any loss resulting from an incorrect wallet address, incorrect network selection, or user error shall be the sole responsibility of the sender.\n\n"
    "**Paysafecard Transactions**\n"
    "• Paysafecard PINs, codes, or QR codes must be transmitted exclusively through private/direct messages (DMs).\n\n"
    "• If a Paysafecard code is shared in a public channel or any location accessible to third parties and is subsequently redeemed by another individual, the exchanger shall bear no liability and shall not be obligated to provide compensation or reimbursement.\n\n"
    "• All Paysafecard codes submitted for exchange must be valid, unused, and unredeemed at the time of submission.\n\n"
    "• Any used, invalid, partially redeemed, or otherwise compromised Paysafecard code may be rejected at the exchanger's sole discretion.\n\n"
    "**Limitation of Liability**\n"
    "• The exchanger shall not be held liable for losses resulting from user negligence, including but not limited to incorrect payment information, incorrect wallet addresses, incorrect currencies, unauthorized disclosure of payment codes, or failure to follow these Terms of Service.\n\n"
    "**By proceeding with an exchange, the user acknowledges and accepts all risks associated with the chosen payment method.**"
)

# ── Keep-alive (Render) ──────────────────────────────────────────────────────
FLASK_PORT = int(os.getenv("PORT", 1000))
