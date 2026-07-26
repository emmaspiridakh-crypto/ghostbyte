r"""
emojis.py
---------
ΟΛΑ τα emoji του bot είναι custom server emoji (όχι unicode/Google emoji).
Αντικατέστησε τα placeholder IDs (0) με τα πραγματικά IDs των custom emoji
του server σου. Format: "<:name:id>" (ή "<a:name:id>" αν είναι animated).

Πώς παίρνεις το ID ενός emoji: γράψε \:emoji_name: σε ένα channel με backslash
μπροστά (π.χ. \:verify:) και στείλε το μήνυμα -- θα σου δείξει το raw format.

Αν κάποιο emoji λείπει/δεν έχει ρυθμιστεί ακόμα, η emoji() επιστρέφει "" ώστε
να μην σκάει το bot -- απλά δεν θα φαίνεται emoji σε εκείνο το σημείο.
"""

EMOJIS = {
    "verify": {
        "verify": "<a:verify:1530853377162874980>",
        "verified": "<a:verified:1530853377162874980>",
        "already": "<:already:1530529572389523556>",
    },
    "ticket": {
        "ticket": "<:ticket:1530489816121086013>",
        "lang": "<:language:1530854961699622963>",
        "greek": "<:greek:1530693092665983117>",
        "english": "<:english:1530693068406263848>",
        "owner": "<:owner:1530855356790603826>",
        "support": "<a:support:1530489609954529310>",
        "partnership": "<:partnership:1530489296619049010>",
        "buy": "<:buy:1530489480233095198>",
        "close": "<:close:1530489016351199234>",
        "ping": "<a:ping:1530529285532549221>",
        "open": "<a:open:1530489063662944336>",
        "category": "<:category:1530489524084281374>",
    },
    "welcome": {
        "welcome": "<a:welcome:1530489142188707890>",
        "members": "<:members:1530490177531674725>",
    },
    "review": {
        "review": "<:review:1530856651135914085>",
        "star": "<:star:1530693543880949942>",
        "star_empty": "<:star_empty:>",
        "submit": "<:submit:1530529572389523556>",
    },
    "suggestion": {
        "suggestion": "<:suggestion:1530857462989590579>",
        "upvote": "<:upvote:1530489269339291689>",
        "downvote": "<:downvote:1530489237831548960>",
    },
    "tos": {
        "document": "<:document:1530909736537690205>",
        "exchange": "<:exchange:1530692764852027574>",
    },
    "logs": {
        "voice_join": "<a:voice_join:1530489063662944336>",
        "voice_leave": "<a:voice_leave:1530489082327859220>",
        "channel": "<:channel:1530489524084281374>",
        "message": "<:message:1530858202722340865>",
        "role": "<:role:1530490177531674725>",
        "ticket": "<:ticket_log:1530488914903564480>",
        "ban": "<:ban:1530858390023311381>",
        "unban": "<:unban:1530858390023311381>",
        "timeout": "<:timeout:1530858573918376057>",
        "untimeout": "<:untimeout:1530858573918376057>",
        "kick": "<:kick:1530858684983283772>",
        "mod": "<:mod:1530489105719361670>",
    },
    "mod": {
        "say": "<:say:1530858202722340865>",
        "dm": "<:dm:1530858202722340865>",
    },
    "giveaway": {
        "giveaway": "<:giveaway:1530859401471070238>",
        "join": "<:join:1530490386991288420>",
        "leave": "<:leave:1530490360848191568>",
        "info": "<:info:1530854961699622963>",
        "edit": "<:edit:1530859806045245501>",
        "reroll": "<a:reroll:1530692764852027574>",
        "end": "<:end:1530489016351199234>",
        "participants": "<:participants:1530490177531674725>",
        "prize": "<:prize:1530860462181322905>",
        "host": "<:host:1530855356790603826>",
        "winners_count": "<:winners_count:1530856651135914085>",
        "entries": "<:entries:1530490177531674725>",
        "time": "<:time:1530529338402017351>",
        "id": "<:id:1530860850808885389>",
        "role": "<:role_req:1530490177531674725>",
        "winner": "<:winner:1530862864255029250>",
    },
    "general": {
        "success": "<:success:1530529572389523556>",
        "error": "<a:error:1530489401317003284>",
        "loading": "<a:loading:1530692764852027574>",
        "arrow": "<:arrow:1530489524084281374>",
    },
}


def emoji(category: str, name: str) -> str:
    """Επιστρέφει το custom emoji string, ή "" αν δεν έχει ρυθμιστεί (ID == 0)."""
    value = EMOJIS.get(category, {}).get(name, "")
    if value.endswith(":0>"):
        return ""
    return value
