"""Joint External Debt Hub (JEDH) connector.

JEDH is jointly produced by BIS, IMF, OECD and the World Bank and is served as
World Bank DataBank source id 54 (code JED) via the v2 Advanced Data API. There
are ~28 SDMX-style series (debt instruments) covering ~175 reporting economies
at quarterly frequency.

Fetch shape: stateless full re-pull. The whole corpus is small (~hundreds of
thousands of observations) and the API exposes no incremental/since filter, so
we re-fetch every series in full each run and overwrite. Revisions and late
corrections are picked up for free.

Published raw assets:
- `series`: the current JEDH indicator catalog.
- `values`: a long-format table of (country, series, time, value) observations
  across every series the source lists.
"""

from datetime import date
import json

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)

BASE = "https://api.worldbank.org/v2"
SOURCE_ID = "54"
PER_PAGE = 20000
MAX_PAGES_ABS = 500  # safety ceiling per series; raises if the source grows past expectation

SERIES_SCHEMA = pa.schema([
    ("series_code", pa.string()),
    ("series_name", pa.string()),
    ("unit", pa.string()),
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("source_note", pa.string()),
    ("source_organization", pa.string()),
    ("topics_json", pa.string()),
])

VALUES_SCHEMA = pa.schema([
    ("country_code", pa.string()),
    ("country_name", pa.string()),
    ("series_code", pa.string()),
    ("series_name", pa.string()),
    ("time_label", pa.string()),
    ("year", pa.int16()),
    ("quarter", pa.int8()),
    ("period_start", pa.date32()),
    ("source_last_updated", pa.string()),
    ("value", pa.float64()),
])


def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _series_catalog() -> list[dict]:
    """Discover the current JEDH series catalog."""
    data = _get_json(
        f"{BASE}/sources/{SOURCE_ID}/indicators",
        {"format": "json", "per_page": 20000, "page": 1},
    )
    # Indicator catalog uses the [pageInfo, rows] envelope.
    rows = data[1] if isinstance(data, list) and len(data) > 1 and data[1] else []
    if not rows:
        raise AssertionError("JEDH indicator catalog returned no series ids")
    return rows


def _series_ids() -> list[str]:
    return [r["id"] for r in _series_catalog() if r.get("id")]


def _series_rows() -> list[dict]:
    rows = []
    for rec in _series_catalog():
        source = rec.get("source") or {}
        rows.append({
            "series_code": rec.get("id"),
            "series_name": rec.get("name"),
            "unit": rec.get("unit"),
            "source_id": source.get("id"),
            "source_name": source.get("value"),
            "source_note": rec.get("sourceNote"),
            "source_organization": rec.get("sourceOrganization"),
            "topics_json": json.dumps(rec.get("topics") or [], sort_keys=True),
        })
    return rows


def _period_parts(time_label: str | None) -> tuple[int | None, int | None, date | None]:
    if not time_label or len(time_label) != 6 or time_label[4] != "Q":
        return None, None, None
    try:
        year = int(time_label[:4])
        quarter = int(time_label[5])
    except ValueError:
        return None, None, None
    if quarter not in {1, 2, 3, 4}:
        return None, None, None
    return year, quarter, date(year, (quarter - 1) * 3 + 1, 1)


def _parse_rows(series_id: str, data: dict) -> list[dict]:
    out = []
    rows = (data.get("source") or {}).get("data") or []
    source_last_updated = data.get("lastupdated")
    for rec in rows:
        fields = {}
        for v in rec.get("variable", []):
            fields[v.get("concept")] = (v.get("id"), v.get("value"))
        country = fields.get("Country", (None, None))
        series = fields.get("Series", (series_id, None))
        time = fields.get("Time", (None, None))
        time_label = time[1]
        year, quarter, period_start = _period_parts(time_label)
        raw_val = rec.get("value")
        out.append({
            "country_code": country[0],
            "country_name": country[1],
            "series_code": series[0],
            "series_name": series[1],
            "time_label": time_label,  # e.g. "2025Q3"
            "year": year,
            "quarter": quarter,
            "period_start": period_start,
            "source_last_updated": source_last_updated,
            "value": float(raw_val) if raw_val is not None else None,
        })
    return out


def _fetch_series(series_id: str) -> list[dict]:
    url = f"{BASE}/sources/{SOURCE_ID}/country/all/series/{series_id}/time/all"
    page = 1
    collected = []
    while True:
        data = _get_json(url, {"format": "json", "per_page": PER_PAGE, "page": page})
        pages = int(data.get("pages") or 1)
        collected.extend(_parse_rows(series_id, data))
        if page >= pages:
            break
        page += 1
        if page > MAX_PAGES_ABS:
            raise AssertionError(
                f"series {series_id} exceeded MAX_PAGES_ABS={MAX_PAGES_ABS} "
                f"(pages reported: {pages}) — source grew past expectation"
            )
    return collected


def fetch_series(node_id: str) -> None:
    rows = _series_rows()
    if not rows:
        raise AssertionError("JEDH series catalog produced 0 rows")
    table = pa.Table.from_pylist(rows, schema=SERIES_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    series_ids = _series_ids()
    rows = []
    for sid in series_ids:
        rows.extend(_fetch_series(sid))
    if not rows:
        raise AssertionError("JEDH fetch produced 0 observations across all series")
    table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="joint-external-debt-hub-series", fn=fetch_series, kind="download"),
    NodeSpec(id="joint-external-debt-hub-values", fn=fetch_values, kind="download"),
]
