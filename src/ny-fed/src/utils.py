"""Shared HTTP + parsing helpers for the NY Fed Markets API connector.

Single REST mechanism: https://markets.newyorkfed.org/api (no auth, JSON).
Two endpoint shapes are used across datasets:

  * date-range search ('.../search.json?startDate=&endDate=') paged in <=89-day
    windows (an undocumented per-request cap; the legacy connector chunked the
    same way).
  * snapshot endpoints (SOMA, primary-dealer history) hit directly.

These helpers are shared by 2+ node files; per-dataset field sets, fetch bodies,
and schemas live in the individual node modules.
"""

from datetime import date, timedelta

from subsets_utils import get, transient_retry

BASE = "https://markets.newyorkfed.org/api"
CHUNK_DAYS = 89  # undocumented per-request range cap; page history in windows


@transient_retry()
def get_json(path: str):
    resp = get(f"{BASE}/{path}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def date_chunks(start: date, end: date):
    cur = start
    while cur <= end:
        chunk_end = min(cur + timedelta(days=CHUNK_DAYS), end)
        yield cur, chunk_end
        cur = chunk_end + timedelta(days=1)


def search(path_template: str, *key_path: str, start: date):
    """Yield every record from a date-range search endpoint across the full
    history (start..today), drilling into the nested envelope via key_path."""
    today = date.today()
    for c_start, c_end in date_chunks(start, today):
        path = path_template.format(
            startDate=c_start.isoformat(), endDate=c_end.isoformat()
        )
        payload = get_json(path)
        node = payload
        for k in key_path:
            node = node.get(k, {}) if isinstance(node, dict) else {}
        if isinstance(node, list):
            yield from node


def project(row: dict, fields: tuple[str, ...], extra: dict | None = None) -> dict:
    """Normalize a raw record to a fixed key set (missing -> None) so the NDJSON
    asset has a stable column list for the SQL transform to read."""
    out = {f: row.get(f) for f in fields}
    if extra:
        out.update(extra)
    return out


def flatten_operations(records, parent_fields, detail_fields, *, results_only=True):
    """One output row per detail entry (parent fields repeated); operations
    with no details emit a single aggregate row."""
    for op in records:
        if results_only and op.get("auctionStatus") != "Results":
            continue
        parent = {f: op.get(f) for f in parent_fields}
        details = op.get("details") or []
        if details:
            for d in details:
                row = dict(parent)
                row.update({f: d.get(f) for f in detail_fields})
                yield row
        else:
            row = dict(parent)
            row.update({f: None for f in detail_fields})
            yield row
