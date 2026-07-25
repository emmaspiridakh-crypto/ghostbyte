# Shop Discord Bot

Πλήρες bot με: Verify, Tickets (2 γλώσσες), Welcome, Logs (ξεχωριστά channels),
Reviews, Suggestions, Mod commands (`!`), Giveaways. Components V2 παντού,
custom emoji (όχι Google), SQLite persistence (δεν χάνει δεδομένα σε restart),
Flask keep-alive για Render.

## 1. Εγκατάσταση

```bash
pip install -r requirements.txt
```

> ⚠️ Τα Components V2 (`ui.LayoutView`, `ui.Container`, `ui.MediaGallery`, `ui.Section`,
> `ui.Thumbnail`) χρειάζονται πρόσφατο discord.py. Αν το `pip install discord.py`
> δεν σου δώσει αυτά τα attributes, βάλε στο requirements.txt αντί για
> `discord.py>=2.6.0`:
> `discord.py @ git+https://github.com/Rapptz/discord.py.git`

## 2. Turso (persistence — υποχρεωτικό)

Το bot χρησιμοποιεί [Turso](https://turso.tech) (hosted SQLite/libSQL) αντί για
τοπικό αρχείο, ώστε τα δεδομένα (tickets, reviews, suggestions, giveaways,
votes) να **μην χάνονται ποτέ** σε redeploy/restart — δουλεύει και στο Render
free plan, που δεν έχει persistent disks.

Χρειάζεσαι 2 environment variables (π.χ. στο Render → Environment, ή τοπικά
σε `.env` / export):

```
TURSO_DATABASE_URL=libsql://<το-db-σου>.turso.io
TURSO_AUTH_TOKEN=<το-token-σου>
```

⚠️ Ποτέ μην τα γράψεις hardcoded μέσα σε αρχείο κώδικα που ανεβαίνει σε
public repo.

## 3. Ρύθμιση (config.py)

Άνοιξε το `config.py` και συμπλήρωσε **όλα** τα IDs (τώρα είναι `0` παντού):

- `BOT_TOKEN` — βάλτο σαν environment variable `BOT_TOKEN` στο Render (μην το γράψεις hardcoded στο αρχείο σε public repo)
- `OWNERSHIP_ROLE_ID`, `MANAGER_ROLE_ID`, `CEO_ROLE_ID`, `COCEO_ROLE_ID`, `STAFF_TEAM_ROLE_IDS`
- `VERIFY_ROLE_ID`
- `TICKET_TYPES[...]["category_id"]` — 5 Discord categories (owner, contact_support, partnership, buy, seller)
- `WELCOME_CHANNEL_ID`
- `REVIEW_OUTPUT_CHANNEL_ID`
- `SUGGESTION_CHANNEL_ID`
- `LOG_CHANNELS` — 12 ξεχωριστά channels (voice, channel, message, role, ticket, ban, unban, timeout, untimeout, kick, mod, giveaway)
- Όλα τα `*_BANNER_URL` / `*_THUMBNAIL_URL`

## 4. Custom Emoji

Άνοιξε το `emojis.py`. Όλα είναι placeholders της μορφής `<:name:0>`.
Αντικατέστησε το `0` με το πραγματικό ID του κάθε custom emoji από τον server
σου (γράψε `\:emoji_name:` σε ένα channel για να δεις το raw format).
Όσο ένα emoji έχει ID `0`, το bot απλά δεν εμφανίζει emoji σε εκείνο το σημείο
(δεν σκάει).

## 5. Τρέξιμο τοπικά (χωρίς Docker)

```bash
python main.py
```

## 6. Τρέξιμο με Docker (τοπικά)

```bash
cp .env.example .env
# γέμισε το .env με BOT_TOKEN / TURSO_DATABASE_URL / TURSO_AUTH_TOKEN
docker compose up --build
```

Ή χωρίς compose:

```bash
docker build -t shopbot .
docker run --env-file .env -p 1000:1000 shopbot
```

## 7. Deploy στο Render με Docker (Free plan)

1. New → Web Service → Connect το repo σου
2. Runtime: **Docker** (το Render εντοπίζει αυτόματα το `Dockerfile`)
3. Environment variables:
   - `BOT_TOKEN=<το token σου>`
   - `TURSO_DATABASE_URL=<το url σου>`
   - `TURSO_AUTH_TOKEN=<το token σου>`
4. Δεν χρειάζεται persistent disk — τα δεδομένα ζουν στο Turso, όχι τοπικά.
5. Για να μην κοιμάται το free service: βάλε δωρεάν monitor στο
   [UptimeRobot](https://uptimerobot.com) (HTTP check στο URL του Render
   service σου, κάθε 5 λεπτά).

## 8. Πρώτη ρύθμιση των panels (μία φορά — μετά μένουν για πάντα)

Μέσα στο Discord, σαν Ownership:
- `/verify-panel` στο verify channel
- `/ticket-panel` στο ticket channel
- `/review-panel` στο review channel
- `/tos-panel` στο ToS channel
- `/giveaway create` για giveaway

Auto Role: δεν χρειάζεται panel/command — μόλις γεμίσεις το
`config.AUTO_ROLE_IDS`, δίνεται αυτόματα σε κάθε νέο μέλος που μπαίνει.

Τα panels είναι **persistent** — δουλεύουν κανονικά ακόμα κι αν το bot κάνει
restart/redeploy, χωρίς να χρειάζεται να τα ξαναστείλεις. Όλα τα δεδομένα
(tickets, reviews, suggestions, giveaways, votes) είναι στο **Turso**, οπότε
δεν χάνονται ποτέ, ανεξάρτητα από το πόσες φορές κάνεις redeploy το container.

## 9. Δομή αρχείων

```
main.py                    → entry point
config.py                  → όλες οι ρυθμίσεις (IDs, URLs, κείμενα)
emojis.py                  → custom emoji IDs
keep_alive.py               → Flask keep-alive (Render)
Dockerfile                  → image build
docker-compose.yml           → τοπικό dev/run
.env.example                 → template για BOT_TOKEN / Turso credentials
utils/permissions.py          → έλεγχος ρόλων
utils/logs.py                 → κεντρικό logging σε ξεχωριστά channels
utils/db.py                    → Turso (libSQL) wrapper
cogs/verify.py
cogs/autorole.py
cogs/tickets.py
cogs/welcome.py
cogs/tos.py
cogs/logging_events.py        → voice/channel/message/role logs
cogs/moderation.py             → ban/unban/timeout/untimeout/kick/dmall/say/say2
cogs/reviews.py
cogs/suggestions.py
cogs/giveaways.py              → (το δικό σου αρχείο, όπως το έστειλες)
```

## 10. Σημειώσεις για τα tickets

- Το πρώτο panel (`/ticket-panel`) δείχνει 2 κουμπιά γλώσσας.
- Μετά την επιλογή γλώσσας, ανοίγει (ephemeral) το panel με dropdown
  categories: Owner, Contact/Support, Partnership, Buy, Seller.
- Partnership & Buy: μόνο CEO/CO-CEO βλέπουν το channel.
- Owner, Contact/Support, Seller: `STAFF_TEAM_ROLE_IDS` βλέπουν το channel.
  (Άλλαξέ το ανά κατηγορία στο `config.TICKET_TYPES` αν θες διαφορετικά.)
- Close/Ping μπορεί να τα κάνει **μόνο staff**, όχι ο χρήστης που άνοιξε το ticket.
- Το close στέλνει DM στον χρήστη και διαγράφει το channel μετά από 5 δευτ.
- Το ping κάνει mention στο channel **και** στέλνει DM.
