"""
utils/permissions.py
---------------------
Μικρά βοηθητικά για έλεγχο ρόλων.
"""

from __future__ import annotations
import discord


def has_roles(member: discord.Member, role_ids) -> bool:
    """True αν το member έχει έστω ΕΝΑΝ από τα role_ids."""
    if not member or not role_ids:
        return False
    member_role_ids = {r.id for r in member.roles}
    return any(rid in member_role_ids for rid in role_ids if rid)
