"""ISM (Institute for Supply Management) — Report On Business diffusion indices.

ISM's own site is paywalled, so this connector reads the DBnomics mirror
(provider code ``ISM``, REST API v22). The provider exposes 23 datasets — 12
Manufacturing and 11 Non-manufacturing components — each a small set of monthly
series: the headline index plus the %higher/%same/%lower/net diffusion
breakdown.

Shape: **stateless full re-pull** (shape 1). The whole corpus is ~23 datasets /
~70 series / a few thousand monthly observations — a few KB each — so we re-fetch
every dataset in full every run and overwrite. No watermark, no cursor: monthly
revisions and late corrections are picked up for free.

One ``DOWNLOAD_SPEC`` per dataset fetches that dataset's series with embedded
observations and writes a **long-format** raw parquet (one row per
series × month). The matching ``TRANSFORM_SPEC`` pivots that long raw into a
**wide** published table — ``date`` plus one column per metric (e.g. ``pmi``,
``index``, ``pct_higher``, ``pct_same``, ``pct_lower``, ``net``). DuckDB's
dynamic ``PIVOT`` derives the columns from the data, so each dataset gets its
own column list without hardcoding.
"""

import re
from datetime import date

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_PROVIDER = "ISM"
_BASE = "https://api.db.nomics.world/v22"
_PAGE = 1000  # DBnomics default/limit; datasets here have <=21 series

# Entity union — the 23 DBnomics ISM dataset codes (rank-active subsets).
from constants import ENTITY_IDS

# Long-format raw schema — one row per (series, month). The transform pivots
# `metric` into columns, so it stays stable even if a dataset gains a series.
_SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("metric", pa.string()),
        ("series_code", pa.string()),
        ("series_name", pa.string()),
        ("value", pa.float64()),
    ]
)


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _metric_slug(name: str) -> str:
    """Clean column label from a DBnomics series_name.

    '% Higher' -> 'pct_higher', 'Index' -> 'index', 'PMI' -> 'pmi',
    'Capital Expenditures; 30 Days' -> 'capital_expenditures_30_days'.
    """
    s = (name or "").strip().lower().replace("%", "pct").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "value"


def _coerce_value(v):
    """DBnomics encodes missing observations as the string 'NA'."""
    if v is None or isinstance(v, str):
        return None
    return float(v)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_code = node_id[len("ism-"):]

    rows: list[dict] = []
    offset = 0
    while True:
        payload = _get_json(
            f"{_BASE}/series/{_PROVIDER}/{dataset_code}",
            {"observations": 1, "limit": _PAGE, "offset": offset},
        )
        series_block = payload["series"]
        docs = series_block["docs"]
        for s in docs:
            metric = _metric_slug(s.get("series_name"))
            scode = s.get("series_code")
            sname = s.get("series_name")
            days = s.get("period_start_day", [])
            vals = s.get("value", [])
            for day, raw_val in zip(days, vals):
                val = _coerce_value(raw_val)
                if val is None:
                    continue  # skip 'NA' / missing observations
                rows.append(
                    {
                        "date": date.fromisoformat(day),  # date32 wants datetime.date
                        "metric": metric,
                        "series_code": scode,
                        "series_name": sname,
                        "value": val,
                    }
                )

        num_found = series_block.get("num_found", len(docs))
        offset += len(docs)
        if not docs or offset >= num_found:
            break

    if not rows:
        raise AssertionError(f"{asset}: DBnomics returned no observations for {dataset_code}")

    table = pa.Table.from_pylist(rows, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ism-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published wide table per dataset: date + one column per metric.
# Dynamic PIVOT derives the column set from the `metric` values in the raw.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            PIVOT (
                SELECT date, metric, value
                FROM "{s.id}"
                WHERE value IS NOT NULL
            )
            ON metric
            USING first(value)
            GROUP BY date
            ORDER BY date
        ''',
        key=("date",),
        temporal="date",
    )
    for s in DOWNLOAD_SPECS
]
