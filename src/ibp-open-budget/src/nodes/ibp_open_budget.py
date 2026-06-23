"""International Budget Partnership — Open Budget Survey (via World Bank Data360).

Single subset: `values`, the long-format Open Budget Survey observations across
all 6 IBP_OBS indicators (Open Budget Index / transparency, country rank, public
participation, overall/legislative/audit oversight) x ~125 countries x survey
rounds 2006-2023.

Fetch shape: stateless full re-pull. The whole corpus is ~6 indicators x <1000
rows each (a few thousand rows total, well under a megabyte), so we re-fetch
every indicator in full each run and overwrite. No watermark, no incremental
filter (the Data360 data endpoint exposes none), no freshness short-circuit
(that is the maintain step's job).

Raw is stored faithfully as parquet with the source's string-typed fields
(OBS_VALUE and TIME_PERIOD arrive as strings); the SQL transform does the
casting and null-dropping so a shape change fails loudly there.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

DATASET_ID = "IBP_OBS"
BASE = "https://data360api.worldbank.org/data360"
PAGE_SIZE = 1000
MAX_PAGES_ABS = 100  # safety ceiling per indicator (~100k rows); raises if exceeded

# Raw schema — the source's fields kept as delivered (strings for the numeric
# fields, which the transform casts). Declared once; every indicator conforms.
SCHEMA = pa.schema([
    ("indicator_code", pa.string()),
    ("ref_area", pa.string()),
    ("time_period", pa.string()),
    ("obs_value", pa.string()),
    ("unit_measure", pa.string()),
    ("obs_status", pa.string()),
    ("latest_data", pa.bool_()),
])


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _discover_indicators():
    codes = _get_json(f"{BASE}/indicators", datasetId=DATASET_ID)
    if not isinstance(codes, list) or not codes:
        raise ValueError(f"unexpected indicators response: {codes!r}")
    return [str(c) for c in codes]


def _fetch_indicator(code):
    """Page through every observation for one indicator via the skip offset."""
    rows = []
    for page in range(MAX_PAGES_ABS):
        body = _get_json(
            f"{BASE}/data",
            DATABASE_ID=DATASET_ID,
            INDICATOR=code,
            skip=page * PAGE_SIZE,
        )
        chunk = body.get("value") if isinstance(body, dict) else None
        if not chunk:
            break
        for rec in chunk:
            rows.append({
                "indicator_code": rec.get("INDICATOR") or code,
                "ref_area": rec.get("REF_AREA"),
                "time_period": rec.get("TIME_PERIOD"),
                "obs_value": rec.get("OBS_VALUE"),
                "unit_measure": rec.get("UNIT_MEASURE"),
                "obs_status": rec.get("OBS_STATUS"),
                "latest_data": rec.get("LATEST_DATA"),
            })
        if len(chunk) < PAGE_SIZE:
            break
    else:
        raise RuntimeError(
            f"{code}: hit MAX_PAGES_ABS={MAX_PAGES_ABS} without draining — "
            f"source grew past expectations, raise the ceiling deliberately"
        )
    return rows


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows = []
    for code in _discover_indicators():
        rows.extend(_fetch_indicator(code))
    if not rows:
        raise RuntimeError("IBP_OBS returned no observations across any indicator")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ibp-open-budget-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ibp-open-budget-values-transform",
        deps=["ibp-open-budget-values"],
        sql='''
            SELECT DISTINCT
                indicator_code,
                ref_area                         AS country_iso3,
                CAST(time_period AS INTEGER)     AS year,
                CAST(obs_value AS DOUBLE)        AS value,
                unit_measure,
                obs_status
            FROM "ibp-open-budget-values"
            WHERE obs_value IS NOT NULL
              AND obs_value <> ''
              AND lower(obs_value) <> 'nan'
              AND time_period IS NOT NULL
        ''',
    ),
]
