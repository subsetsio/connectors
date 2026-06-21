"""Post-DAG health invariants for the Bank of Israel connector.

These run in-connector after the download specs execute, reading raw through the
same loader the download nodes wrote with (Parquet). They catch silent
degradation that file existence alone misses: empty payloads, the SDMX endpoint
switching format, or a flow losing its observation column.
"""

from subsets_utils import load_raw_parquet

# Columns SDMX-CSV carries for every BOI.STATISTICS dataflow.
_UNIVERSAL_COLS = {"SERIES_CODE", "FREQ", "TIME_PERIOD", "OBS_VALUE"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow's bulk pull should hold observations. 0 rows means the
    endpoint changed format or the dataflow stopped publishing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_universal_columns_present(spec_ids):
    """Each raw asset must carry the four columns universal across all
    dataflows. Missing one means the CSV header shifted underneath us."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        missing = _UNIVERSAL_COLS - set(table.column_names)
        assert not missing, f"{sid}: missing universal columns {sorted(missing)}"


def test_obs_value_mostly_numeric(spec_ids):
    """OBS_VALUE is stored as a string but should parse as a number for the
    vast majority of rows. A wholesale failure means we grabbed the wrong
    column or the payload is metadata, not data."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        values = table.column("OBS_VALUE").to_pylist()[:5000]
        numeric = 0
        for v in values:
            if v in (None, ""):
                continue
            try:
                float(v)
                numeric += 1
            except (TypeError, ValueError):
                pass
        assert numeric > 0, f"{sid}: no numeric OBS_VALUE in first {len(values)} rows"
