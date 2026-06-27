from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {"series_key", "date", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every collection's raw asset should hold rows. An empty payload usually
    means the public endpoint changed shape or the collection went private."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """The long-format contract is (series_key, date, value). A missing column
    means the flatten step or the API response shape broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert EXPECTED_COLUMNS.issubset(cols), f"{sid}: columns {cols} missing {EXPECTED_COLUMNS - cols}"


def test_date_format_monthly(spec_ids):
    """Every KOF series date is a 'YYYY-MM' month string. A different length
    means the API switched granularity/format and the transform CAST will break."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dates = table.column("date").drop_null().to_pylist()
        bad = [d for d in dates[:5000] if not (isinstance(d, str) and len(d) == 7 and d[4] == "-")]
        assert not bad, f"{sid}: {len(bad)} dates not in 'YYYY-MM' form, e.g. {bad[:3]}"
