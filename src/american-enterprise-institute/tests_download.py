from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows. An empty payload
    usually means the Cloudflare challenge fired or the xlsx link moved."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_indicators_shape(spec_ids):
    """The housing-market-indicators workbook is broad: many metros and a long
    quarterly history. A tiny table means the workbook was truncated."""
    sid = "american-enterprise-institute-housing-market-indicators"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) >= 10000, f"{sid}: only {len(table)} rows; expected >=10000"
    metros = set(table.column("metro").to_pylist())
    assert len(metros) >= 90, f"{sid}: only {len(metros)} distinct metros; expected ~100"
    segments = set(table.column("segment").to_pylist())
    assert segments <= {"Overall", "Entry-level", "Move-up"}, f"unexpected segments: {segments}"
