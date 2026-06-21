"""Health-invariant tests for the Bundesbank download assets.

Each dataflow is fetched as long SDMX-CSV and written to parquet with the SCHEMA
declared in src/nodes/bundesbank.py. These tests catch silent degradation the
file-existence check misses: empty payloads, a format switch that drops the value
column, or observations with no parseable series key.

Most dataflows write one asset file (`bundesbank-<id>.parquet`); BBKRT writes one
file per vintage year (`bundesbank-bbkrt-<year>.parquet`). `_asset_tables` loads
whichever layout is present so every spec is checked the same way.
"""
from subsets_utils import list_raw_files, load_raw_parquet

EXPECTED_COLS = {
    "dataflow", "series_id", "title", "time_period",
    "time_format", "unit", "unit_mult", "decimals", "value",
}


def _asset_tables(sid):
    """All parquet tables behind a spec id — the single `<sid>.parquet` file, or
    the `<sid>-*.parquet` batch files (BBKRT's per-year layout)."""
    rels = list_raw_files(f"{sid}.parquet") or list_raw_files(f"{sid}-*.parquet")
    return [load_raw_parquet(rel[:-len(".parquet")]) for rel in rels]


def test_all_assets_nonempty(spec_ids):
    """Every spec must produce at least one file with rows. An empty payload
    usually means the SDMX media type stopped being honoured or a flowRef 404'd."""
    for sid in spec_ids:
        tables = _asset_tables(sid)
        assert tables, f"{sid}: no raw parquet files written"
        assert sum(len(t) for t in tables) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_columns(spec_ids):
    """The kept-column contract must survive — a format switch that renamed or
    dropped BBK_ID / OBS_VALUE would surface here, not as published garbage."""
    for sid in spec_ids:
        for table in _asset_tables(sid):
            cols = set(table.column_names)
            assert EXPECTED_COLS <= cols, f"{sid}: missing columns {EXPECTED_COLS - cols}"


def test_series_and_values_present(spec_ids):
    """A real time series has non-null series ids and at least some numeric
    values; all-null on either column means the parse silently broke."""
    for sid in spec_ids:
        tables = _asset_tables(sid)
        total = sum(len(t) for t in tables)
        series_nulls = sum(t.column("series_id").null_count for t in tables)
        value_nulls = sum(t.column("value").null_count for t in tables)
        assert series_nulls < total, f"{sid}: all series_id are null"
        assert value_nulls < total, f"{sid}: all values are null"
