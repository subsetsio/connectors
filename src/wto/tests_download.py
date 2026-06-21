"""Post-DAG health invariants for the WTO bulk downloads.

Raw assets are large (BaTiS is tens of millions of rows), so these checks read
only parquet metadata via raw_parquet_localpath — never load the full table into
memory."""

import pyarrow.parquet as pq

from subsets_utils import raw_parquet_localpath

# Minimum row counts: the smallest of these files already has well over 10k
# rows; anything near zero means a truncated download or a changed format.
_MIN_ROWS = {
    "wto-merchandise-values-annual": 100_000,
    "wto-merchandise-indices-annual": 50_000,
    "wto-services-annual": 100_000,
    "wto-batis-bpm6": 1_000_000,
    "wto-tismos": 100_000,
}

# A couple of stable, asset-specific columns whose disappearance signals the
# upstream CSV header changed under us.
_REQUIRED_COLS = {
    "wto-merchandise-values-annual": {"IndicatorCode", "Reporter", "Year", "Value"},
    "wto-merchandise-indices-annual": {"IndicatorCode", "Reporter", "Year", "Value"},
    "wto-services-annual": {"IndicatorCode", "Reporter", "Year", "Value"},
    "wto-batis-bpm6": {"Reporter", "Partner", "Flow", "Year", "Balanced_value"},
    "wto-tismos": {"FLOW", "REPORTER", "INDICATOR", "YEAR", "MODE", "VALUE"},
}


def test_raw_assets_have_expected_rows(spec_ids):
    """Each raw parquet must hold at least its floor of rows; a tiny payload
    means the bulk file was truncated or the endpoint changed silently."""
    for sid in spec_ids:
        with raw_parquet_localpath(sid) as path:
            n = pq.ParquetFile(path).metadata.num_rows
        floor = _MIN_ROWS.get(sid, 1)
        assert n >= floor, f"{sid}: {n} rows < expected floor {floor}"


def test_raw_assets_have_expected_columns(spec_ids):
    """The source CSV headers are stable; if a required column vanished the
    transform would publish wrong/empty data."""
    for sid in spec_ids:
        with raw_parquet_localpath(sid) as path:
            cols = set(pq.ParquetFile(path).schema.names)
        required = _REQUIRED_COLS.get(sid, set())
        missing = required - cols
        assert not missing, f"{sid}: missing expected columns {missing} (have {sorted(cols)})"
