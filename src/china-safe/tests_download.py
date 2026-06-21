from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's raw parquet must hold rows. Empty means advQuery2 returned
    the anti-automation block page or the InfoTable layout changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values(spec_ids):
    """Columns present, values are real numbers, period codes are 4 (annual) or
    6 (monthly) digits — guards against parse drift in the HTML table."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert {"table_code", "project", "period", "value"} <= cols, f"{sid}: cols {cols}"
        values = table.column("value").to_pylist()
        assert any(v is not None for v in values), f"{sid}: all values null"
        periods = table.column("period").to_pylist()
        bad = [p for p in periods if not (p and p.isdigit() and len(p) in (4, 6))]
        assert not bad, f"{sid}: {len(bad)} malformed period codes e.g. {bad[:3]}"


def test_reserves_has_long_history(spec_ids):
    """FX reserves (C2) should carry a long monthly series — a sharp drop in
    coverage means the period enumeration silently truncated."""
    sid = "china-safe-c2"
    if sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 200, f"{sid}: only {len(table)} reserve observations; expected >=200"
