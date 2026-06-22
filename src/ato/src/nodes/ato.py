"""ATO connector — data.gov.au CKAN catalog.

Each entity is a recurring ATO statistical table, collapsed across its
per-income-year editions (one CKAN resource per year). We build only from the
flat **CSV** editions: ATO published header-first CSV exports of its detailed
tables (industry financial ratios, activity-statement ratios, etc.), mainly for
the 2014-15 and 2015-16 income years. We download each year's CSV file
directly, tag every row with its `income_year`, and write the union as one
NDJSON raw asset. NDJSON (not parquet) because column sets drift across years
for the same table, so a fixed schema would be wrong. The XLSX editions are
deliberately skipped — their datastore parses are banner-polluted and their
workbooks are multi-sheet, neither cleanly SQL-readable.

Fetch shape: **stateless full re-pull** (decision shape 1). The whole corpus is
small (datastore tables are tens of thousands of rows at most) and the source
exposes no useful per-record delta filter, so every refresh re-pulls in full and
overwrites — late ATO revisions are picked up for free.

The transform is a thin pass-through: datastore values are all text and the
209 tables are mutually heterogeneous, so generic per-column typing isn't
possible here; the SQL publishes the unioned rows as-is (light reshape only).
"""

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from constants import ENTITY_IDS
from utils import build_groups, csv_rows, safe_columns


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("ato-"):]

    groups = build_groups()
    resources = groups.get(entity_id)
    if not resources:
        # coverage is validated up front, so a miss here means the catalog
        # grouping drifted from collect — a bug, not a transient condition.
        raise RuntimeError(f"{node_id}: entity {entity_id!r} not found in live catalog")

    rows = []
    raw_keys: dict[str, None] = {}  # ordered set: first-seen column order
    for res in resources:
        if res["format"] != "CSV" or not res.get("url"):
            continue  # build only from the clean flat CSV editions
        for row in csv_rows(res["url"], res["income_year"]):
            rows.append(row)
            for k in row:
                raw_keys.setdefault(k, None)

    # Editions of the same table drift their column sets year to year; build one
    # union schema (missing -> null) with Delta-safe names, all stored as text
    # (the raw CSV is untyped). An explicit pyarrow schema keeps even very wide
    # tables (hundreds of columns) intact, which JSON auto-inference does not.
    colmap = safe_columns(raw_keys)
    schema = pa.schema([(colmap[k], pa.string()) for k in raw_keys])
    records = [
        {colmap[k]: (None if row.get(k) is None else str(row.get(k))) for k in raw_keys}
        for row in rows
    ]
    table = pa.Table.from_pylist(records, schema=schema)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ato-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
