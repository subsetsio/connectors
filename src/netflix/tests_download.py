"""Health-invariant tests for the Netflix Top 10 connector.

These run post-DAG in-connector and read raw through the same loaders the
download nodes used. They catch silent degradation that file existence misses:
truncated downloads, format switches, columns going all-null.
"""

from subsets_utils import load_raw_parquet

# Loose floors: the corpus only grows. If a download truncates after a partial
# response, these trip. Set well below current real sizes (global ~10k,
# countries ~482k, most-popular 40).
_MIN_ROWS = {
    "netflix-global-weekly": 8000,
    "netflix-countries-weekly": 400000,
    "netflix-most-popular": 30,
}


def test_raw_row_floors(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, (
            f"{sid}: {len(table)} rows < expected floor {floor} "
            "(truncated download or format change?)"
        )


def test_global_metrics_present(spec_ids):
    """The global file must carry weekly_hours_viewed for (effectively) every
    row — it is populated for the whole history, unlike runtime/views which are
    empty pre-2023. All-null here means the column moved or parsing broke."""
    sid = "netflix-global-weekly"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    col = table.column("weekly_hours_viewed")
    non_null = len(col) - col.null_count
    assert non_null > 0.9 * len(col), (
        f"{sid}: weekly_hours_viewed non-null only {non_null}/{len(col)}"
    )


def test_countries_coverage(spec_ids):
    """The per-country file should span dozens of distinct countries; a collapse
    to a handful means the file was truncated or the wrong file was served."""
    sid = "netflix-countries-weekly"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    distinct = len(set(table.column("country_iso2").to_pylist()))
    assert distinct >= 50, f"{sid}: only {distinct} distinct countries"
