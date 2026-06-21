"""Health invariants for the CMHC StatCan bulk-CSV download nodes."""

from subsets_utils import load_raw_parquet

# StatCan long-format frame columns that must be present on every raw table.
_REQUIRED_COLS = {"REF_DATE", "GEO", "VALUE", "UOM"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's raw parquet must hold rows. An empty payload means the
    StatCan zip changed shape, the product was retired, or the download
    silently truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_statcan_frame_columns_present(spec_ids):
    """Every table must carry the fixed StatCan long-format columns. Missing
    ones mean the CSV format drifted and the transform would break."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _REQUIRED_COLS - cols
        assert not missing, f"{sid}: missing StatCan columns {missing}"


def test_value_has_some_numbers(spec_ids):
    """At least one non-null VALUE per table — an all-null VALUE column means
    the data payload was dropped while headers survived."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("VALUE")
        assert col.null_count < table.num_rows, f"{sid}: VALUE is entirely null"
