"""Shared HTTP + parse helpers for the DHS Program connector.

The DHS public REST API (https://api.dhsprogram.com/rest/dhs/) is a single
no-auth JSON service. Every subset pages the same envelope shape
(TotalPages/Data) and shares the same empty-string -> None normalization, so
that logic lives here once and the per-subset node files import it.
"""
from __future__ import annotations

from subsets_utils import get, transient_retry

BASE = "https://api.dhsprogram.com/rest/dhs"

PERPAGE = 5000
# Safety ceiling: the biggest country today is ~5 pages at perpage=5000. 100
# pages (~500k records for one country) means the source grew far past
# expectations — fail loudly rather than silently truncate.
MAX_PAGES = 100


@transient_retry()
def _fetch_json(url: str, **params) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_all(url: str, **filters) -> list[dict]:
    """Page a DHS resource fully, returning every record. The JSON envelope
    carries TotalPages/Data; we follow it to the last page."""
    filters.setdefault("f", "json")
    filters.setdefault("perpage", PERPAGE)
    rows: list[dict] = []
    page = 1
    while True:
        envelope = _fetch_json(url, page=page, **filters)
        rows.extend(envelope.get("Data") or [])
        total_pages = envelope.get("TotalPages") or 1
        if page >= total_pages:
            break
        page += 1
        if page > MAX_PAGES:
            raise RuntimeError(
                f"{url} (filters={filters}) exceeded MAX_PAGES={MAX_PAGES} "
                f"(TotalPages={total_pages}) — source grew past expectations"
            )
    return rows


def clean(record: dict) -> dict:
    """Normalize empty-string sentinels to None so each JSON field keeps one
    consistent type across all batch files (the DHS API uses '' for absent
    numeric values)."""
    return {k: (None if v == "" else v) for k, v in record.items()}
