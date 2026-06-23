"""Homebrew anonymous analytics connector.

Source: https://formulae.brew.sh/api/analytics/{category}/{window}.json — static
JSON ranked reports served via Fastly CDN (no auth, no rate limit). Each report
is a ranked table {number, <item>, count, percent} for one rolling time window.

Shape: stateless full re-pull every run. The whole corpus is ~5 categories x 3
windows, each at most ~80k rows of tiny JSON (a few MB) — re-fetching everything
each refresh is trivially cheap, and these are rolling-window aggregates with no
incremental delta filter anyway. No state, no watermark.

Granularity: the 30d/90d/365d windows share one schema, so each category is ONE
download asset holding all three windows (the window is a column value, not a
separate asset). `count`/`percent` arrive as strings upstream and are parsed to
numeric here so the parquet raw is already typed.
"""

from datetime import date

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

BASE = "https://formulae.brew.sh/api/analytics"
WINDOWS = ["30d", "90d", "365d"]

# entity_id -> the JSON key naming each ranked item in that category's response.
# (URL category path == entity id for every entity in the union.)
ITEM_KEY = {
    "install": "formula",
    "install-on-request": "formula",
    "build-error": "formula",
    "cask-install": "cask",
    "os-version": "os_version",
}

# Raw is uniform across categories: the semantic item name (formula/cask/
# os_version) is stored in a generic `item` column and re-aliased per category
# in the transform SQL.
SCHEMA = pa.schema([
    ("window", pa.string()),
    ("window_start", pa.date32()),
    ("window_end", pa.date32()),
    ("rank", pa.int32()),
    ("item", pa.string()),
    ("count", pa.int64()),
    ("percent", pa.float64()),
])


@transient_retry()
def _fetch_window(category: str, window: str) -> dict:
    resp = get(f"{BASE}/{category}/{window}.json", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _parse_count(raw) -> int:
    # Upstream renders counts comma-grouped, e.g. "5,596,763".
    return int(str(raw).replace(",", ""))


def fetch_report(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    category = node_id[len("homebrew-analytics-"):]
    item_key = ITEM_KEY[category]

    rows = []
    for window in WINDOWS:
        payload = _fetch_window(category, window)
        # ISO date strings ("2026-05-24") -> date objects; the date32 schema
        # columns are backed by int days and cannot coerce raw strings.
        start = date.fromisoformat(payload["start_date"])
        end = date.fromisoformat(payload["end_date"])
        items = payload["items"]
        if not items:
            raise AssertionError(f"{category}/{window}: empty items array")
        for it in items:
            rows.append({
                "window": window,
                "window_start": start,
                "window_end": end,
                "rank": int(it["number"]),
                "item": it[item_key],
                "count": _parse_count(it["count"]),
                # percent is a plain decimal string ("2.03", "44", "0").
                "percent": float(it["percent"]),
            })

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="homebrew-analytics-install", fn=fetch_report, kind="download"),
    NodeSpec(id="homebrew-analytics-install-on-request", fn=fetch_report, kind="download"),
    NodeSpec(id="homebrew-analytics-build-error", fn=fetch_report, kind="download"),
    NodeSpec(id="homebrew-analytics-cask-install", fn=fetch_report, kind="download"),
    NodeSpec(id="homebrew-analytics-os-version", fn=fetch_report, kind="download"),
]


def _transform_sql(download_id: str, item_name: str) -> str:
    # Thin parse-and-type pass: rename the generic `item` column to its semantic
    # name, keep one row per (window, rank). Drop the long tail of count==0 rows
    # (formulae/casks observed 0 times in the window carry no signal).
    # "window" is a reserved keyword in DuckDB (window functions) — quote it.
    return f'''
        SELECT
            "window"                   AS window,
            CAST(window_start AS DATE) AS window_start,
            CAST(window_end   AS DATE) AS window_end,
            CAST(rank AS INTEGER)      AS rank,
            item                       AS {item_name},
            CAST(count AS BIGINT)      AS count,
            CAST(percent AS DOUBLE)    AS percent
        FROM "{download_id}"
        WHERE count > 0
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id, ITEM_KEY[s.id[len("homebrew-analytics-"):]]),
    )
    for s in DOWNLOAD_SPECS
]
