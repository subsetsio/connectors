"""Crossref reference registries — Open Funder Registry, journal-title registry,
and registered-member registry, all from the public, no-auth Crossref REST API.

  - crossref-funders   Open Funder Registry (~45.7k rows)   — stateless full pull
  - crossref-journals  journal-title registry (~166.8k)     — stateless full pull
  - crossref-members   registered-org registry (~32.8k)     — stateless full pull

The three registries are small reference catalogs: cursor-page each to completion
every run and overwrite. They share one parametric fetcher (`fetch_registry`)
driven by the `_REGISTRIES` config table.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _first, _iter_pages

# Safety ceiling — detects the source growing past expectations and RAISES; it
# never silently truncates. 2000 * 1000 = 2M rows; registries are <200k.
MAX_REGISTRY_PAGES = 2000


# --- flatteners -------------------------------------------------------------


def _flatten_funder(it: dict) -> dict:
    return {
        "funder_id": it.get("id"),
        "name": it.get("name"),
        "location": it.get("location"),
        "uri": it.get("uri"),
    }


def _flatten_journal(it: dict) -> dict:
    counts = it.get("counts") or {}
    return {
        "title": it.get("title"),
        "issn": _first(it.get("ISSN")),
        "publisher": it.get("publisher"),
        "total_dois": counts.get("total-dois"),
        "current_dois": counts.get("current-dois"),
        "backfile_dois": counts.get("backfile-dois"),
    }


def _flatten_member(it: dict) -> dict:
    counts = it.get("counts") or {}
    return {
        "member_id": it.get("id"),
        "primary_name": it.get("primary-name"),
        "location": it.get("location"),
        "total_dois": counts.get("total-dois"),
        "current_dois": counts.get("current-dois"),
        "backfile_dois": counts.get("backfile-dois"),
    }


# --- registry downloads (stateless full pull) -------------------------------

_FUNDERS_SCHEMA = pa.schema([
    ("funder_id", pa.string()),
    ("name", pa.string()),
    ("location", pa.string()),
    ("uri", pa.string()),
])

_JOURNALS_SCHEMA = pa.schema([
    ("title", pa.string()),
    ("issn", pa.string()),
    ("publisher", pa.string()),
    ("total_dois", pa.int64()),
    ("current_dois", pa.int64()),
    ("backfile_dois", pa.int64()),
])

_MEMBERS_SCHEMA = pa.schema([
    ("member_id", pa.int64()),
    ("primary_name", pa.string()),
    ("location", pa.string()),
    ("total_dois", pa.int64()),
    ("current_dois", pa.int64()),
    ("backfile_dois", pa.int64()),
])

# node_id -> (endpoint path, flattener, arrow schema)
_REGISTRIES = {
    "crossref-funders": ("funders", _flatten_funder, _FUNDERS_SCHEMA),
    "crossref-journals": ("journals", _flatten_journal, _JOURNALS_SCHEMA),
    "crossref-members": ("members", _flatten_member, _MEMBERS_SCHEMA),
}


def fetch_registry(node_id: str) -> None:
    """Cursor-page a small Crossref reference registry to completion, flatten to
    a fixed schema, and overwrite the single raw parquet. Stateless full re-pull:
    these catalogs are small and carry no useful incremental filter, so every run
    picks up revisions for free."""
    path, flatten, schema = _REGISTRIES[node_id]
    rows: list[dict] = []
    for items in _iter_pages(path, params={}, max_pages=MAX_REGISTRY_PAGES):
        rows.extend(flatten(it) for it in items)
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, node_id)


# --- specs ------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="crossref-funders", fn=fetch_registry, kind="download"),
    NodeSpec(id="crossref-journals", fn=fetch_registry, kind="download"),
    NodeSpec(id="crossref-members", fn=fetch_registry, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="crossref-funders-transform",
        deps=["crossref-funders"],
        sql='''
            SELECT
                CAST(funder_id AS VARCHAR) AS funder_id,
                name,
                location,
                uri
            FROM "crossref-funders"
            WHERE funder_id IS NOT NULL AND name IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="crossref-journals-transform",
        deps=["crossref-journals"],
        sql='''
            SELECT
                title,
                issn,
                publisher,
                CAST(total_dois AS BIGINT)    AS total_dois,
                CAST(current_dois AS BIGINT)  AS current_dois,
                CAST(backfile_dois AS BIGINT) AS backfile_dois
            FROM "crossref-journals"
            WHERE title IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="crossref-members-transform",
        deps=["crossref-members"],
        sql='''
            SELECT
                CAST(member_id AS BIGINT)     AS member_id,
                primary_name,
                location,
                CAST(total_dois AS BIGINT)    AS total_dois,
                CAST(current_dois AS BIGINT)  AS current_dois,
                CAST(backfile_dois AS BIGINT) AS backfile_dois
            FROM "crossref-members"
            WHERE member_id IS NOT NULL
        ''',
    ),
]
