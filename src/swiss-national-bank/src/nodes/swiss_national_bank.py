"""Swiss National Bank (SNB) data portal download nodes.

The SNB portal publishes statistical time-series "cubes". Each accepted cube is
fetched as one JSON document and stored as normalized parquet: one row per
series observation, with the original period label preserved and a best-effort
period_start date for freshness/model profiling.
"""

from __future__ import annotations

import json
import re
from datetime import date

import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "swiss-national-bank"
BASE_URL = "https://data.snb.ch/api"

SCHEMA = pa.schema(
    [
        ("cube_id", pa.string()),
        ("series_key", pa.string()),
        ("series_label", pa.string()),
        ("dimensions_json", pa.string()),
        ("frequency", pa.string()),
        ("unit", pa.string()),
        ("scale", pa.string()),
        ("period", pa.string()),
        ("period_start", pa.date32()),
        ("value", pa.float64()),
    ]
)

_MONTH_RE = re.compile(r"^(\d{4})-(\d{2})$")
_DAY_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_QUARTER_RE = re.compile(r"^(\d{4})-Q([1-4])$")
_YEAR_RE = re.compile(r"^(\d{4})$")


def _spec_id(cube_id: str) -> str:
    return f"{SLUG}-{cube_id.lower().replace('_', '-')}"


def _cube_for(node_id: str) -> str:
    for cube_id in ENTITY_IDS:
        if _spec_id(cube_id) == node_id:
            return cube_id
    raise KeyError(f"no cube for node id {node_id!r}")


def _cube_url(cube_id: str) -> str:
    if "@" in cube_id:
        warehouse_id = cube_id.replace("@", ".")
        return f"{BASE_URL}/warehouse/cube/{warehouse_id}/data/json/en"
    return f"{BASE_URL}/cube/{cube_id}/data/json/en"


def _period_start(period: str | None) -> date | None:
    if not period:
        return None
    if m := _DAY_RE.match(period):
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if m := _MONTH_RE.match(period):
        return date(int(m.group(1)), int(m.group(2)), 1)
    if m := _QUARTER_RE.match(period):
        return date(int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, 1)
    if m := _YEAR_RE.match(period):
        return date(int(m.group(1)), 1, 1)
    return None


def fetch_one(node_id: str) -> None:
    cube_id = _cube_for(node_id)
    resp = get(_cube_url(cube_id), timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()

    rows = []
    for series in payload.get("timeseries", []) or []:
        meta = series.get("metadata") or {}
        header = series.get("header") or []
        dimensions = [
            {
                "dimension": item.get("dim"),
                "value": item.get("dimItem"),
            }
            for item in header
        ]
        label = " | ".join(item.get("dimItem") or "" for item in header)
        for point in series.get("values", []) or []:
            period = point.get("date")
            value = point.get("value")
            rows.append(
                {
                    "cube_id": cube_id,
                    "series_key": meta.get("key"),
                    "series_label": label,
                    "dimensions_json": json.dumps(
                        dimensions, ensure_ascii=True, separators=(",", ":")
                    ),
                    "frequency": meta.get("frequency"),
                    "unit": meta.get("unit"),
                    "scale": meta.get("scale"),
                    "period": period,
                    "period_start": _period_start(period),
                    "value": float(value) if value is not None else None,
                }
            )

    save_raw_parquet(pa.Table.from_pylist(rows, schema=SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(entity_id), fn=fetch_one, kind="download")
    for entity_id in ENTITY_IDS
]
