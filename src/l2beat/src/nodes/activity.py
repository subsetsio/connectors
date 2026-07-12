"""L2Beat activity — long-format daily transaction activity per project (+ aggregate).

Stateless full re-pull every run: ~116 projects fetched one slug at a time, plus
an ecosystem-wide aggregate stored as a synthetic project.
"""

import time
from datetime import UTC, datetime

import httpx
import pyarrow as pa

from subsets_utils import TRANSIENT_EXC, save_raw_parquet
from utils import (
    BASE,
    THROTTLE_S,
    _AGGREGATE_SLUG,
    _chart_rows,
    _get_json,
    _project_slugs,
)

_ACTIVITY_SCHEMA = pa.schema([
    ("project_slug", pa.string()),
    ("timestamp", pa.int64()),
    ("date", pa.date32()),
    ("tx_count", pa.int64()),
    ("uops_count", pa.int64()),
])


def _int(value) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    return None


def _date_from_timestamp(value: int):
    return datetime.fromtimestamp(value, UTC).date()


def _activity_rows_for(slug: str, url: str) -> list[dict]:
    payload = _get_json(url)
    if payload.get("success") is False:
        print(f"[l2beat-activity] {slug}: success=false ({payload.get('error')!r}), skipping")
        return []
    types, data = _chart_rows(payload)
    if not data:
        return []
    idx = {t: i for i, t in enumerate(types)}
    out = []
    for row in data:
        def col(name):
            i = idx.get(name)
            return row[i] if i is not None and i < len(row) else None
        ts = col("timestamp")
        if ts is None:
            continue
        ts = int(ts)
        out.append({
            "project_slug": slug,
            "timestamp": ts,
            "date": _date_from_timestamp(ts),
            "tx_count": _int(col("count")),
            "uops_count": _int(col("uopsCount")),
        })
    return out


def fetch_activity(node_id: str) -> None:
    asset = node_id
    slugs = _project_slugs()
    rows: list[dict] = []
    skipped: list[str] = []

    try:
        rows.extend(_activity_rows_for(_AGGREGATE_SLUG, f"{BASE}/scaling/activity?range=max"))
    except Exception as exc:  # noqa: BLE001 - logged, aggregate is non-critical
        print(f"[l2beat-activity] aggregate fetch failed: {type(exc).__name__}: {exc}")
    time.sleep(THROTTLE_S)

    for i, slug in enumerate(slugs):
        url = f"{BASE}/scaling/activity/{slug}?range=max"
        try:
            rows.extend(_activity_rows_for(slug, url))
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            print(f"[l2beat-activity] {slug}: HTTP {code} after retries, skipping")
            skipped.append(slug)
        except TRANSIENT_EXC as exc:
            print(f"[l2beat-activity] {slug}: {type(exc).__name__} after retries, skipping")
            skipped.append(slug)
        if i < len(slugs) - 1:
            time.sleep(THROTTLE_S)

    if skipped:
        print(f"[l2beat-activity] skipped {len(skipped)}/{len(slugs)} projects: {skipped}")
    table = pa.Table.from_pylist(rows, schema=_ACTIVITY_SCHEMA)
    save_raw_parquet(table, asset)
