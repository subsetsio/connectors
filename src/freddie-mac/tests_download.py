from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty payloads usually mean the
    endpoint switched format or started returning an error page."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_fmhpi_geo_types_and_size(spec_ids):
    """FMHPI must cover all three geographic levels and ~270k monthly rows.
    A collapse to one geo level or a tiny row count means the master file
    changed shape or the download truncated."""
    sid = "freddie-mac-house-price-index"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) > 200_000, f"FMHPI only {len(table)} rows; expected >200k"
    geo = set(table.column("geo_type").to_pylist())
    assert {"US", "State", "CBSA"} <= geo, f"FMHPI geo_type set unexpected: {geo}"


def test_pmms_rows_and_rate_range(spec_ids):
    """PMMS is weekly since 1971 (~2800 rows). 30yr fixed rate must sit in a
    sane band; out-of-range or a tiny row count means parsing or the ragged
    column layout broke."""
    sid = "freddie-mac-mortgage-rates"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) > 2_500, f"PMMS only {len(table)} rows; expected >2500"
    rates = [v for v in table.column("pmms30").to_pylist() if v is not None]
    assert rates, "PMMS has no non-null 30yr rates"
    assert min(rates) >= 1.0, f"PMMS 30yr rate too low: {min(rates)}"
    assert max(rates) <= 25.0, f"PMMS 30yr rate too high: {max(rates)}"
