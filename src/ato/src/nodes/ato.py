"""ATO connector — data.gov.au CKAN catalog.

Each accepted entity maps to one logical ATO resource group from data.gov.au.
Flat CSV-only groups are written as wide Parquet tables with an `income_year`
column. Workbook/archive groups are written as a fixed-schema cell table with
resource, sheet, row and column coordinates; ATO workbooks are human-oriented
and often have sheet-specific banner/header layouts, so a cell table is the
stable SQL-readable raw contract at download time.

Fetch shape: stateless full re-pull. The corpus is modest and the source
exposes no useful per-record delta filter, so every refresh re-pulls in full and
overwrites; late ATO revisions are picked up on the next scheduled run.
"""

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from constants import ENTITY_IDS
from utils import build_groups, csv_rows, safe_columns, tabular_cell_rows


CELL_SCHEMA = pa.schema([
    ("source_resource_id", pa.string()),
    ("source_resource_name", pa.string()),
    ("source_format", pa.string()),
    ("source_url", pa.string()),
    ("income_year", pa.string()),
    ("sheet_name", pa.string()),
    ("row_number", pa.int32()),
    ("column_number", pa.int32()),
    ("value", pa.string()),
])


def _is_csv_resource(resource: dict) -> bool:
    fmt = (resource.get("format") or "").upper()
    url = (resource.get("url") or "").lower()
    return ("CSV" in fmt or url.endswith(".csv")) and "ZIP" not in fmt and not url.endswith(".zip")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("ato-"):]

    groups = build_groups()
    resources = groups.get(entity_id)
    if not resources:
        # coverage is validated up front, so a miss here means the catalog
        # grouping drifted from collect — a bug, not a transient condition.
        raise RuntimeError(f"{node_id}: entity {entity_id!r} not found in live catalog")

    resources = [res for res in resources if res.get("url")]
    if not resources:
        raise RuntimeError(f"{node_id}: no downloadable resources for {entity_id!r}")

    if all(_is_csv_resource(res) for res in resources):
        rows = []
        raw_keys: dict[str, None] = {}  # ordered set: first-seen column order
        for res in resources:
            for row in csv_rows(res["url"], res["income_year"]):
                rows.append(row)
                for k in row:
                    raw_keys.setdefault(k, None)

        if not rows:
            raise RuntimeError(f"{node_id}: no CSV rows fetched for {entity_id!r}")

        # Editions of the same table drift their column sets year to year; build
        # one union schema (missing -> null) with Delta-safe names, all text.
        colmap = safe_columns(raw_keys)
        schema = pa.schema([(colmap[k], pa.string()) for k in raw_keys])
        records = [
            {colmap[k]: (None if row.get(k) is None else str(row.get(k))) for k in raw_keys}
            for row in rows
        ]
        save_raw_parquet(pa.Table.from_pylist(records, schema=schema), asset)
        return

    records = []
    for res in resources:
        records.extend(tabular_cell_rows(res))
    if not records:
        raise RuntimeError(f"{node_id}: no workbook/archive cells fetched for {entity_id!r}")
    save_raw_parquet(pa.Table.from_pylist(records, schema=CELL_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ato-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# Every row is tagged with its edition's `income_year` (see fetch_one), so it is
# the uniform observation-period column across all of these heterogeneous
# statistical tables. Grains differ per table and are not reliably keyable, so
# only temporal is declared.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        temporal="income_year",
    )
    for s in DOWNLOAD_SPECS
]
