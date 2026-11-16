"""Founder Support Tracker API.

Deployed as a single Vercel Python function. vercel.json rewrites every
/api/* path here, and FastAPI does the routing.
Layers: routes (this file) -> repository (_repository.py) -> Postgres (_db.py).
"""
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(__file__))  # let sibling _modules import on Vercel and locally

import psycopg  # noqa: E402
from fastapi import Depends, FastAPI, HTTPException, Query, Response  # noqa: E402

import _repository as repo  # noqa: E402
from _db import get_conn  # noqa: E402
from _schemas import (  # noqa: E402
    Partner, RequestCreate, RequestUpdate, Status, SupportRequest,
)

app = FastAPI(title="Founder Support Tracker API", docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.get("/api/health")
def health(conn: psycopg.Connection = Depends(get_conn)):
    conn.execute("select 1")
    return {"status": "ok"}


@app.get("/api/partners", response_model=list[Partner])
def list_partners(conn: psycopg.Connection = Depends(get_conn)):
    return repo.list_partners(conn)


@app.get("/api/stats")
def stats(conn: psycopg.Connection = Depends(get_conn)):
    return repo.status_counts(conn)


@app.get("/api/requests", response_model=list[SupportRequest])
def list_requests(
    status: Optional[Status] = None,
    q: Optional[str] = Query(default=None, max_length=100),
    conn: psycopg.Connection = Depends(get_conn),
):
    return repo.list_requests(conn, status, q)


@app.get("/api/requests/{request_id}", response_model=SupportRequest)
def get_request(request_id: int, conn: psycopg.Connection = Depends(get_conn)):
    row = repo.get_request(conn, request_id)
    if not row:
        raise HTTPException(404, "Request not found")
    return row


@app.post("/api/requests", response_model=SupportRequest, status_code=201)
def create_request(body: RequestCreate, conn: psycopg.Connection = Depends(get_conn)):
    try:
        return repo.create_request(conn, body.model_dump())
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(400, "Unknown partner_id")


@app.patch("/api/requests/{request_id}", response_model=SupportRequest)
def update_request(request_id: int, body: RequestUpdate, conn: psycopg.Connection = Depends(get_conn)):
    try:
        row = repo.update_request(conn, request_id, body.model_dump(exclude_unset=True))
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(400, "Unknown partner_id")
    if not row:
        raise HTTPException(404, "Request not found")
    return row


@app.delete("/api/requests/{request_id}", status_code=204)
def delete_request(request_id: int, conn: psycopg.Connection = Depends(get_conn)):
    if not repo.delete_request(conn, request_id):
        raise HTTPException(404, "Request not found")
    return Response(status_code=204)
