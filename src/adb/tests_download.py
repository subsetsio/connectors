"""Health invariants for the ADB KIDB raw downloads.

These run post-DAG, in-connector, and read raw through the same loader the
download node used (parquet). They catch silent degradation that file
existence alone misses: empty payloads, a truncated CSV that lost its data
columns, or a format switch that drops the observation value.
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLUMNS = {
    "DATAFLOW", "FREQ", "INDICATOR", "ECONOMY_CODE", "TIME_PERIOD",
    "OBS_VALUE", "UNIT", "UNIT_MULT", "DECIMALS", "OBS_STATUS",
    "REF_YEAR", "BASE_YEAR", "DATA_SOURCE", "METHODOLOGY", "FOOTNOTE",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow returned rows. An empty table means the wildcard query
    silently stopped matching (format change, blocked, or bad dataflow id)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_schema_intact(spec_ids):
    """The full SDMX-CSV column set must survive parsing — a header drift would
    quietly strip OBS_VALUE/INDICATOR and break every downstream transform."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing raw columns {sorted(missing)}"


def test_obs_value_mostly_present(spec_ids):
    """OBS_VALUE is the payload — it should be populated on the vast majority
    of rows. A mostly-empty column signals a parse or encoding regression."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("OBS_VALUE").to_pylist()
        nonempty = sum(1 for v in vals if v not in (None, ""))
        assert nonempty >= 0.8 * len(vals), (
            f"{sid}: only {nonempty}/{len(vals)} rows have OBS_VALUE"
        )
