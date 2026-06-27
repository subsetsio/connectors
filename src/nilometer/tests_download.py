from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. An empty payload usually means
    the cran mirror moved the file or the R `ts()` literal changed shape and the
    c(...) parse silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_minima_span_and_shape(spec_ids):
    """The Roda Nilometer minima are a continuous yearly series 622-1284.
    Guards against a truncated download or a misaligned year index."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = table.column("year").to_pylist()
        assert len(years) >= 655, f"{sid}: only {len(years)} rows; expected ~663"
        assert min(years) == 622, f"{sid}: first year {min(years)}, expected 622"
        assert max(years) == 1284, f"{sid}: last year {max(years)}, expected 1284"
        assert len(set(years)) == len(years), f"{sid}: duplicate years present"
        levels = table.column("min_level").to_pylist()
        assert all(l is not None for l in levels), f"{sid}: null min_level present"
        assert all(700 < l < 1700 for l in levels), f"{sid}: min_level out of expected gauge range"
