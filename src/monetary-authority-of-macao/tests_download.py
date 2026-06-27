"""Health invariants for the AMCM raw assets, run post-DAG inside the connector."""
from subsets_utils import load_raw_parquet

_COLS = {"series", "period", "year", "part", "date", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every worksheet is a multi-period time series; an empty parquet means the
    CDN URL re-resolution failed silently or the sheet layout changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_is_long_format(spec_ids):
    """The parser always emits the long-format schema; a missing column means a
    fetch fn wrote a different shape."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert _COLS <= cols, f"{sid}: missing columns {_COLS - cols}"


def test_values_are_finite(spec_ids):
    """Values are parsed numerics; all-null or NaN-only columns indicate the
    numeric-cell detection broke for this sheet."""
    import math
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value").to_pylist()
        good = [v for v in col if v is not None and not math.isnan(v)]
        assert good, f"{sid}: no finite values"
