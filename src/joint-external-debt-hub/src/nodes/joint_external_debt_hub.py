"""Joint External Debt Hub (JEDH) connector.

JEDH is jointly produced by BIS, IMF, OECD and the World Bank and is served as
World Bank DataBank source id 54 (code JED) via the v2 Advanced Data API. There
are ~28 SDMX-style series (debt instruments) covering ~175 reporting economies
at quarterly frequency.

Fetch shape: stateless full re-pull. The whole corpus is small (~hundreds of
thousands of observations) and the API exposes no incremental/since filter, so
we re-fetch every series in full each run and overwrite. Revisions and late
corrections are picked up for free.

One published subset (`values`): a long-format table of (country, series, time,
value) observations across every series the source lists.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://api.worldbank.org/v2"
SOURCE_ID = "54"
PER_PAGE = 20000
MAX_PAGES_ABS = 500  # safety ceiling per series; raises if the source grows past expectation

SCHEMA = pa.schema([
    ("country_code", pa.string()),
    ("country_name", pa.string()),
    ("series_code", pa.string()),
    ("series_name", pa.string()),
    ("time_label", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _list_series() -> list[str]:
    """Discover the current set of JEDH series ids from the source's indicator catalog."""
    data = _get_json(
        f"{BASE}/sources/{SOURCE_ID}/indicators",
        {"format": "json", "per_page": 20000, "page": 1},
    )
    # Indicator catalog uses the [pageInfo, rows] envelope.
    rows = data[1] if isinstance(data, list) and len(data) > 1 and data[1] else []
    ids = [r["id"] for r in rows if r.get("id")]
    if not ids:
        raise AssertionError("JEDH indicator catalog returned no series ids")
    return ids


def _parse_rows(series_id: str, data: dict) -> list[dict]:
    out = []
    rows = (data.get("source") or {}).get("data") or []
    for rec in rows:
        fields = {}
        for v in rec.get("variable", []):
            fields[v.get("concept")] = (v.get("id"), v.get("value"))
        country = fields.get("Country", (None, None))
        series = fields.get("Series", (series_id, None))
        time = fields.get("Time", (None, None))
        raw_val = rec.get("value")
        out.append({
            "country_code": country[0],
            "country_name": country[1],
            "series_code": series[0],
            "series_name": series[1],
            "time_label": time[1],  # e.g. "2025Q3"
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


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    series_ids = _list_series()
    rows = []
    for sid in series_ids:
        rows.extend(_fetch_series(sid))
    if not rows:
        raise AssertionError("JEDH fetch produced 0 observations across all series")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="joint-external-debt-hub-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="joint-external-debt-hub-values-transform",
        deps=["joint-external-debt-hub-values"],
        sql='''
            SELECT
                country_code,
                country_name,
                series_code,
                series_name,
                time_label,
                CAST(substr(time_label, 1, 4) AS INTEGER)                       AS year,
                CAST(substr(time_label, 6, 1) AS INTEGER)                       AS quarter,
                make_date(
                    CAST(substr(time_label, 1, 4) AS INTEGER),
                    (CAST(substr(time_label, 6, 1) AS INTEGER) - 1) * 3 + 1,
                    1
                )                                                               AS period_start,
                CAST(value AS DOUBLE)                                           AS value
            FROM "joint-external-debt-hub-values"
            WHERE value IS NOT NULL
              AND country_code IS NOT NULL
              AND time_label IS NOT NULL
              AND regexp_full_match(time_label, '[0-9]{4}Q[1-4]')
        ''',
    ),
]
