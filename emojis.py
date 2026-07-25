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
        "verify": "<:verify:0>",
        "verified": "<:verified:0>",
        "already": "<:already:0>",
    },
    "ticket": {
        "ticket": "<:ticket:0>",
        "lang": "<:language:0>",
        "greek": "<:greek:0>",
        "english": "<:english:0>",
        "owner": "<:owner:0>",
        "support": "<:support:0>",
        "partnership": "<:partnership:0>",
        "buy": "<:buy:0>",
        "seller": "<:seller:0>",
        "close": "<:close:0>",
        "ping": "<:ping:0>",
        "open": "<:open:0>",
        "category": "<:category:0>",
    },
    "welcome": {
        "welcome": "<:welcome:0>",
        "members": "<:members:0>",
    },
    "review": {
        "review": "<:review:0>",
        "star": "<:star:0>",
        "star_empty": "<:star_empty:0>",
        "submit": "<:submit:0>",
    },
    "suggestion": {
        "suggestion": "<:suggestion:0>",
        "upvote": "<:upvote:0>",
        "downvote": "<:downvote:0>",
    },
    "logs": {
        "voice_join": "<:voice_join:0>",
        "voice_leave": "<:voice_leave:0>",
        "channel": "<:channel:0>",
        "message": "<:message:0>",
        "role": "<:role:0>",
        "ticket": "<:ticket_log:0>",
        "ban": "<:ban:0>",
        "unban": "<:unban:0>",
        "timeout": "<:timeout:0>",
        "untimeout": "<:untimeout:0>",
        "kick": "<:kick:0>",
        "mod": "<:mod:0>",
    },
    "mod": {
        "say": "<:say:0>",
        "dm": "<:dm:0>",
    },
    "giveaway": {
        "giveaway": "<:giveaway:0>",
        "join": "<:join:0>",
        "leave": "<:leave:0>",
        "info": "<:info:0>",
        "edit": "<:edit:0>",
        "reroll": "<:reroll:0>",
        "end": "<:end:0>",
        "participants": "<:participants:0>",
        "prize": "<:prize:0>",
        "host": "<:host:0>",
        "winners_count": "<:winners_count:0>",
        "entries": "<:entries:0>",
        "time": "<:time:0>",
        "id": "<:id:0>",
        "role": "<:role_req:0>",
        "winner": "<:winner:0>",
    },
    "general": {
        "success": "<:success:0>",
        "error": "<:error:0>",
        "loading": "<:loading:0>",
        "arrow": "<:arrow:0>",
    },
}


def emoji(category: str, name: str) -> str:
    """Επιστρέφει το custom emoji string, ή "" αν δεν έχει ρυθμιστεί (ID == 0)."""
    value = EMOJIS.get(category, {}).get(name, "")
    if value.endswith(":0>"):
        return ""
    return value
