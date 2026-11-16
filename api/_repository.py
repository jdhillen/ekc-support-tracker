"""Data access: all SQL lives here so the route handlers stay thin.

Writes commit explicitly so the data is durable before the HTTP response goes out
(a serverless function may be frozen right after responding).
"""
from typing import Any, Optional

import psycopg
from psycopg import sql

SELECT_REQUEST = """
    select r.*, p.name as partner_name
    from requests r
    left join partners p on p.id = r.partner_id
"""

# Columns a client may change via PATCH (keys come from the Pydantic model, never raw input).
UPDATABLE_COLUMNS = {
    "title", "description", "requester_name", "requester_email", "business_name",
    "category", "priority", "status", "partner_id",
}


def list_partners(conn: psycopg.Connection) -> list[dict]:
    return conn.execute("select id, name, focus from partners order by name").fetchall()


def list_requests(conn: psycopg.Connection, status: Optional[str], q: Optional[str]) -> list[dict]:
    pattern = f"%{q.strip()}%" if q and q.strip() else None
    return conn.execute(
        SELECT_REQUEST
        + """
        where (%(status)s::text is null or r.status = %(status)s)
          and (%(pattern)s::text is null
               or r.title ilike %(pattern)s
               or r.requester_name ilike %(pattern)s
               or r.business_name ilike %(pattern)s)
        order by
          case r.status when 'resolved' then 1 else 0 end,
          case r.priority when 'high' then 0 when 'medium' then 1 else 2 end,
          r.created_at desc
        """,
        {"status": status, "pattern": pattern},
    ).fetchall()


def get_request(conn: psycopg.Connection, request_id: int) -> Optional[dict]:
    return conn.execute(SELECT_REQUEST + " where r.id = %s", (request_id,)).fetchone()


def create_request(conn: psycopg.Connection, data: dict[str, Any]) -> dict:
    columns = list(data.keys())
    query = sql.SQL("insert into requests ({cols}) values ({vals}) returning id").format(
        cols=sql.SQL(", ").join(map(sql.Identifier, columns)),
        vals=sql.SQL(", ").join(sql.Placeholder(c) for c in columns),
    )
    new_id = conn.execute(query, data).fetchone()["id"]
    conn.commit()
    return get_request(conn, new_id)


def update_request(conn: psycopg.Connection, request_id: int, changes: dict[str, Any]) -> Optional[dict]:
    # Explicit null is only meaningful for partner_id (unassign); ignore it elsewhere.
    changes = {
        k: v for k, v in changes.items()
        if k in UPDATABLE_COLUMNS and (v is not None or k == "partner_id")
    }
    if not changes:
        return get_request(conn, request_id)
    assignments = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder(k)) for k in changes]
    assignments.append(sql.SQL("updated_at = now()"))
    query = sql.SQL("update requests set {sets} where id = {id} returning id").format(
        sets=sql.SQL(", ").join(assignments),
        id=sql.Placeholder("_id"),
    )
    row = conn.execute(query, {**changes, "_id": request_id}).fetchone()
    conn.commit()
    return get_request(conn, request_id) if row else None


def delete_request(conn: psycopg.Connection, request_id: int) -> bool:
    deleted = conn.execute("delete from requests where id = %s", (request_id,)).rowcount > 0
    conn.commit()
    return deleted


def status_counts(conn: psycopg.Connection) -> dict[str, int]:
    rows = conn.execute("select status, count(*)::int as n from requests group by status").fetchall()
    counts = {"new": 0, "referred": 0, "in_progress": 0, "resolved": 0}
    counts.update({r["status"]: r["n"] for r in rows})
    return counts
