"""L2Beat tvs — long-format daily Total Value Secured per project (+ aggregate).

Stateless full re-pull every run: the whole corpus is ~116 projects fetched one
slug at a time, plus an ecosystem-wide aggregate stored as a synthetic project.
"""

import time

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, TRANSIENT_EXC, save_raw_parquet
from utils import (
    BASE,
    THROTTLE_S,
    _AGGREGATE_SLUG,
    _chart_rows,
    _get_json,
    _project_slugs,
)

_TVS_SCHEMA = pa.schema([
    ("project_slug", pa.string()),
    ("timestamp", pa.int64()),
    ("native", pa.float64()),
    ("canonical", pa.float64()),
    ("external", pa.float64()),
    ("eth_price", pa.float64()),
])


def _num(value) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _tvs_rows_for(slug: str, url: str) -> list[dict]:
    payload = _get_json(url)
    if payload.get("success") is False:
        print(f"[l2beat-tvs] {slug}: success=false ({payload.get('error')!r}), skipping")
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
        out.append({
            "project_slug": slug,
            "timestamp": int(ts),
            "native": _num(col("native")),
            "canonical": _num(col("canonical")),
            "external": _num(col("external")),
            "eth_price": _num(col("ethPrice")),
        })
    return out


def fetch_tvs(node_id: str) -> None:
    asset = node_id
    slugs = _project_slugs()
    rows: list[dict] = []
    skipped: list[str] = []

    # Ecosystem-wide aggregate (no slug) — same schema, stored as a synthetic project.
    try:
        rows.extend(_tvs_rows_for(_AGGREGATE_SLUG, f"{BASE}/scaling/tvs?range=max"))
    except Exception as exc:  # noqa: BLE001 - logged, aggregate is non-critical
        print(f"[l2beat-tvs] aggregate fetch failed: {type(exc).__name__}: {exc}")
    time.sleep(THROTTLE_S)

    for i, slug in enumerate(slugs):
        url = f"{BASE}/scaling/tvs/{slug}?range=max"
        try:
            rows.extend(_tvs_rows_for(slug, url))
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            if code == 404:  # project genuinely has no tvs series
                print(f"[l2beat-tvs] {slug}: 404, no series, skipping")
                skipped.append(slug)
            else:
                print(f"[l2beat-tvs] {slug}: HTTP {code} after retries, skipping")
                skipped.append(slug)
        except TRANSIENT_EXC as exc:
            print(f"[l2beat-tvs] {slug}: {type(exc).__name__} after retries, skipping")
            skipped.append(slug)
        if i < len(slugs) - 1:
            time.sleep(THROTTLE_S)

    if skipped:
        print(f"[l2beat-tvs] skipped {len(skipped)}/{len(slugs)} projects: {skipped}")
    table = pa.Table.from_pylist(rows, schema=_TVS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="l2beat-tvs", fn=fetch_tvs, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="l2beat-tvs-transform",
        deps=["l2beat-tvs"],
        sql='''
            SELECT
                project_slug,
                CAST(to_timestamp(timestamp) AS DATE) AS date,
                native,
                canonical,
                external,
                COALESCE(native, 0) + COALESCE(canonical, 0) + COALESCE(external, 0) AS total_usd,
                eth_price
            FROM "l2beat-tvs"
            WHERE timestamp IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY project_slug, CAST(to_timestamp(timestamp) AS DATE)
                ORDER BY timestamp DESC
            ) = 1
        ''',
    ),
]
