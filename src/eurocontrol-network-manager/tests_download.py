"""Health-invariant tests for the EUROCONTROL Network Manager raw assets.

Each download node writes one full-snapshot table. These tests catch silent
degradation that mere file existence misses: empty/truncated payloads and the
loss of the year dimension every PRU dataset carries.
"""
from subsets_utils import load_raw_parquet, load_raw_ndjson

# Datasets persisted as NDJSON (bespoke openpyxl extraction); all others parquet.
_NDJSON = {
    "eurocontrol-network-manager-ansp-financial-data",
    "eurocontrol-network-manager-ace-yearly-operational-data",
}


def _load(sid):
    if sid in _NDJSON:
        rows = load_raw_ndjson(sid)
        return rows, (list(rows[0].keys()) if rows else [])
    table = load_raw_parquet(sid)
    return table, table.column_names


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset must hold rows. An empty payload usually means the
    endpoint changed format or the target sheet went missing."""
    for sid in spec_ids:
        data, _ = _load(sid)
        n = len(data) if sid in _NDJSON else data.num_rows
        assert n > 0, f"{sid}: raw asset has 0 rows"


def test_year_dimension_present(spec_ids):
    """Every PRU dataset is a time series stamped with a year column
    (YEAR for the performance files, Year for the ACE/ANSP workbooks)."""
    for sid in spec_ids:
        _, cols = _load(sid)
        assert any(c in ("YEAR", "Year") for c in cols), (
            f"{sid}: no YEAR/Year column among {cols[:12]}"
        )
