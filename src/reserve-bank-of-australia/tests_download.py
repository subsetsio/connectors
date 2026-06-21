"""Post-DAG health invariants for the RBA connector.

These run in-connector after the DAG, reading raw via the same loader the
download node used (parquet). They catch silent degradation that file
existence alone misses: empty/truncated CSVs, a parser that stopped finding
the data block, or the multi-file subsets losing their partitions.
"""
from subsets_utils import load_raw_parquet

_REQUIRED_COLS = {
    "series_id", "obs_date", "value_text", "source_csv", "partition_key",
}

# Subsets that must carry more than one partition_key (collapsed multi-file).
_MULTI_FILE_IDS = {
    "reserve-bank-of-australia-b12.1.1",
    "reserve-bank-of-australia-b12.2.1",
    "reserve-bank-of-australia-b13.1.1",
    "reserve-bank-of-australia-b13.1.2",
    "reserve-bank-of-australia-b13.2.1",
    "reserve-bank-of-australia-j1-forecasts",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows. An empty payload
    usually means the endpoint switched format or the UA got blocked again."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_series_ids(spec_ids):
    """Long-format schema present and series_id populated — guards against the
    metadata-block parser silently shifting columns."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        missing = _REQUIRED_COLS - set(table.column_names)
        assert not missing, f"{sid}: missing columns {missing}"
        nonnull_ids = table.column("series_id").drop_null()
        assert len(nonnull_ids) == len(table), f"{sid}: rows with null series_id"
        assert len(set(nonnull_ids.to_pylist())) > 0, f"{sid}: no series ids"


def test_multifile_subsets_have_partitions(spec_ids):
    """The collapsed by-country / forecast subsets must retain >1 distinct
    partition_key, else the region/variable fan-in silently dropped members."""
    for sid in _MULTI_FILE_IDS:
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        parts = set(table.column("partition_key").drop_null().to_pylist())
        assert len(parts) > 1, f"{sid}: expected multiple partitions, got {parts}"


def test_dates_parse(spec_ids):
    """obs_date must be ISO yyyy-mm-dd for the vast majority of rows; a spike of
    unparseable dates means a new date format slipped through."""
    import re
    iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dates = table.column("obs_date").to_pylist()
        bad = [d for d in dates if not (d and iso.match(d))]
        assert not bad, f"{sid}: {len(bad)} rows with non-ISO obs_date (e.g. {bad[:3]})"
