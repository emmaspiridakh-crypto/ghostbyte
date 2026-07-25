"""
utils/db.py
------------
Κεντρικό wrapper για Turso (hosted libSQL) — αντικαθιστά το τοπικό aiosqlite,
ώστε τα δεδομένα (tickets, reviews, suggestions, giveaways, ψήφοι) να ΜΗΝ
χάνονται σε redeploy/restart στο Render, ακόμα και χωρίς persistent disk.

ΡΥΘΜΙΣΗ: όρισε 2 environment variables (π.χ. στο Render → Environment):
  TURSO_DATABASE_URL = libsql://xxxxx.turso.io
  TURSO_AUTH_TOKEN   = <το token σου>

ΠΟΤΕ μην τα γράψεις hardcoded μέσα στον κώδικα.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import libsql_client

_client: Optional[libsql_client.Client] = None


def get_client() -> libsql_client.Client:
    global _client
    if _client is None:
        url = os.getenv("TURSO_DATABASE_URL")
        token = os.getenv("TURSO_AUTH_TOKEN")
        if not url or not token:
            raise RuntimeError(
                "Λείπουν τα TURSO_DATABASE_URL / TURSO_AUTH_TOKEN environment variables."
            )
        _client = libsql_client.create_client(url=url, auth_token=token)
    return _client


async def execute(sql: str, args: Optional[list] = None) -> libsql_client.ResultSet:
    """Τρέχει ένα query (INSERT/UPDATE/DELETE/CREATE) και επιστρέφει το ResultSet."""
    client = get_client()
    return await client.execute(sql, args or [])


async def fetch_one(sql: str, args: Optional[list] = None) -> Optional[dict]:
    rs = await execute(sql, args)
    if not rs.rows:
        return None
    return dict(zip(rs.columns, rs.rows[0]))


async def fetch_all(sql: str, args: Optional[list] = None) -> list[dict]:
    rs = await execute(sql, args)
    return [dict(zip(rs.columns, row)) for row in rs.rows]


async def close():
    global _client
    if _client is not None:
        await _client.close()
        _client = None
