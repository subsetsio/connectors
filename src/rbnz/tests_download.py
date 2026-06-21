"""Post-DAG health invariants for the RBNZ connector.

These run in-connector after the download nodes, seeing raw through the same
subsets_utils loaders the fetch used. They catch silent degradation that file
existence alone misses: a Cloudflare block writing nothing, a layout change
producing empty/untyped tables, or the date/value parse silently dropping data.
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLUMNS = {
    "series_code", "option", "file_stem", "sheet", "indicator_label",
    "series_id", "series_name", "unit", "date", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every series must yield rows. An empty asset usually means the workbook
    fetch returned a WAF/challenge page or the xlsx layout changed."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} series have 0 raw rows: {empty[:10]}"


def test_expected_columns(spec_ids):
    """The long-format schema must be intact on every asset."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_value_and_date_non_null(spec_ids):
    """fetch drops null values/dates before writing — confirm none slipped in,
    which would indicate the numeric/date coercion misfired."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.column("value").null_count == 0, f"{sid}: null values present"
        assert table.column("date").null_count == 0, f"{sid}: null dates present"
        assert table.column("indicator_label").null_count == 0, \
            f"{sid}: null indicator_label present"


def test_dates_in_plausible_range(spec_ids):
    """RBNZ history starts in the 20th century and shouldn't run far past now;
    a wildly out-of-range date means the date column was misdetected."""
    import datetime
    lo = datetime.date(1900, 1, 1)
    hi = datetime.date(2100, 1, 1)
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dmin = min(table.column("date").to_pylist())
        dmax = max(table.column("date").to_pylist())
        assert lo <= dmin and dmax <= hi, f"{sid}: date range {dmin}..{dmax} implausible"
