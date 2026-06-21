from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset should hold rows. An empty payload usually means
    the endpoint changed shape, paginated to nothing, or TLS/auth broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_cover_many_series(spec_ids):
    """The long-format observations asset should span many distinct variables;
    a collapse to one variable means the per-variable loop broke."""
    sid = "central-bank-of-argentina-monetary-values"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    distinct = len(set(table.column("idVariable").to_pylist()))
    assert distinct >= 100, f"{sid}: only {distinct} distinct variables; expected hundreds"
