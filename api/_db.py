"""Database connection handling.

Vercel runs this API as a serverless function, so we open one short-lived
connection per request against Supabase's *transaction pooler* (port 6543)
instead of keeping a long-lived pool inside the function.
"""
import os
from collections.abc import Iterator

import psycopg
from psycopg.rows import dict_row


def get_conn() -> Iterator[psycopg.Connection]:
    """FastAPI dependency: yields a connection, commits on success, rolls back on error."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    # prepare_threshold=None: the transaction pooler (PgBouncer) can't use prepared statements.
    with psycopg.connect(url, row_factory=dict_row, prepare_threshold=None, connect_timeout=10) as conn:
        yield conn
