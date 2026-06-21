"""Health invariants for the Banco de Espana raw downloads.

Each raw asset is the long-format reshape of one publication table CSV. These
tests catch silent degradation the harness's file-existence check misses:
empty/truncated extracts, a metadata-header parse that swallowed the data rows,
or a period-label format change that nulls every date.
"""
from subsets_utils import load_raw_parquet

_EXPECTED_COLUMNS = {
    "series_code", "alias", "description", "units",
    "frequency", "period_label", "date", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every table should yield at least a handful of observations. An empty
    extract means the ZIP member was missing or the header parser ate the body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    """All eight long-format columns must be present on every asset."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).schema.names)
        missing = _EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_no_null_values(spec_ids):
    """Missing observations ('_') are dropped at download time, so a non-null
    value is the core invariant. A null here means the value parser broke."""
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value")
        assert col.null_count == 0, f"{sid}: {col.null_count} null values in raw"


def test_dates_mostly_parsed(spec_ids):
    """Spanish period labels must parse to real dates. If a label format
    changed upstream, dates would go null wholesale — trip if >5% are null."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n = len(table)
        if n == 0:
            continue
        nulls = table.column("date").null_count
        assert nulls <= 0.05 * n, f"{sid}: {nulls}/{n} dates failed to parse"
