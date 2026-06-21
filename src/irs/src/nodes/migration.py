"""IRS SOI county-migration / state-migration tables.

Bulk CSVs probed at <prefix>{inflow,outflow}<yyyy>.csv. One parametric fetch
drives both subsets; they share the probe loop and parse, differing only in the
geographic key columns.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import (
    BASE,
    _csv_dicts,
    _fetch,
    _int,
    _num,
    _str,
    _two_digit_years,
    _write_batch,
)


def _migration_schema(node_id: str) -> pa.Schema:
    if node_id == "irs-county-migration":
        geo = [
            ("y2_statefips", pa.string()),
            ("y2_countyfips", pa.string()),
            ("y1_statefips", pa.string()),
            ("y1_countyfips", pa.string()),
            ("y1_state", pa.string()),
            ("y1_countyname", pa.string()),
        ]
    else:  # irs-state-migration
        geo = [
            ("y2_statefips", pa.string()),
            ("y1_statefips", pa.string()),
            ("y1_state", pa.string()),
            ("y1_state_name", pa.string()),
        ]
    return pa.schema(
        [("year", pa.int32()), ("direction", pa.string())]
        + geo
        + [("n1", pa.int64()), ("n2", pa.int64()), ("agi", pa.float64())]
    )


def fetch_migration(node_id: str) -> None:
    asset = node_id
    is_county = node_id == "irs-county-migration"
    prefix = "county" if is_county else "state"
    schema = _migration_schema(node_id)
    geo_cols = [f.name for f in schema if f.name not in ("year", "direction", "n1", "n2", "agi")]

    def to_rows(content: bytes, year: int, direction: str):
        for r in _csv_dicts(content):
            row = {"year": year, "direction": direction}
            for c in geo_cols:
                row[c] = _str(r.get(c))
            row["n1"] = _int(r.get("n1"))
            row["n2"] = _int(r.get("n2"))
            row["agi"] = _num(r.get("agi"))
            yield row

    found = 0
    for y in _two_digit_years(2004):
        pair = f"{(y - 1) % 100:02d}{y % 100:02d}"
        for direction in ("inflow", "outflow"):
            content = _fetch(f"{BASE}/{prefix}{direction}{pair}.csv")
            if content is None:
                continue
            _write_batch(f"{asset}-{pair}-{direction}", schema, to_rows(content, y, direction))
            found += 1
    if not found:
        raise RuntimeError(f"{asset}: discovered no migration files under {BASE}")


DOWNLOAD_SPECS = [
    NodeSpec(id="irs-county-migration", fn=fetch_migration, kind="download"),
    NodeSpec(id="irs-state-migration", fn=fetch_migration, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=f'SELECT * FROM "{s.id}"')
    for s in DOWNLOAD_SPECS
]
