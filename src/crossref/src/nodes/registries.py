"""Crossref reference registries from the public, no-auth Crossref REST API.

  - crossref-funders   Open Funder Registry (~45.7k rows)   — stateless full pull
  - crossref-journals  journal-title registry (~166.8k)     — stateless full pull
  - crossref-members   registered-org registry (~32.8k)     — stateless full pull
  - crossref-types     work-type vocabulary (30 rows)        — stateless full pull

The three registries are small reference catalogs: cursor-page each to completion
every run and overwrite. They share one parametric fetcher (`fetch_registry`)
driven by the `_REGISTRIES` config table.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _first, _get_json, _iter_pages

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


def _flatten_type(it: dict) -> dict:
    return {
        "type_id": it.get("id"),
        "label": it.get("label"),
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

_TYPES_SCHEMA = pa.schema([
    ("type_id", pa.string()),
    ("label", pa.string()),
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


def fetch_types(node_id: str) -> None:
    """Fetch the Crossref work-type vocabulary.

    Unlike the registry routes above, /types is a tiny list endpoint and rejects
    cursor parameters, so it is fetched as a single JSON response.
    """
    page = _get_json("types", {})
    rows = [_flatten_type(it) for it in (page.get("message", {}).get("items") or [])]
    table = pa.Table.from_pylist(rows, schema=_TYPES_SCHEMA)
    save_raw_parquet(table, node_id)
