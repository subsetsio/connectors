"""Health-invariant tests for the GLODAP connector raw assets.

These run post-DAG, in-connector, and load raw data through the same
subsets_utils loader the download node used to write it.
"""
from subsets_utils import load_raw_parquet

# Core scientific columns that must survive parsing — if these vanish, the
# upstream CSV header changed or the typed projection silently dropped them.
_CORE_COLUMNS = {
    "expocode", "cruise", "year", "month", "day",
    "latitude", "longitude", "depth", "pressure",
    "temperature", "salinity", "oxygen", "nitrate", "phosphate",
    "silicate", "tco2", "talk", "doi",
}


def test_bottle_data_nonempty(spec_ids):
    """The merged master file holds ~1.4M samples; an empty or tiny table
    means a truncated/failed download rather than a real product."""
    assert "glodap-bottle-data" in spec_ids, spec_ids
    table = load_raw_parquet("glodap-bottle-data")
    assert len(table) >= 500_000, f"glodap-bottle-data: only {len(table)} rows"


def test_bottle_data_columns(spec_ids):
    """All core scientific columns must be present with the G2 prefix stripped."""
    table = load_raw_parquet("glodap-bottle-data")
    cols = set(table.column_names)
    missing = _CORE_COLUMNS - cols
    assert not missing, f"glodap-bottle-data: missing core columns {sorted(missing)}"


def test_expocode_populated(spec_ids):
    """Every row should carry a cruise expocode; nulls there mean the key
    column was misparsed."""
    table = load_raw_parquet("glodap-bottle-data")
    assert table.column("expocode").null_count == 0, "expocode has nulls"
