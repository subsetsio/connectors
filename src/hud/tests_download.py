"""Health-invariant tests for the HUD connector. Run post-DAG, in-connector."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every program's raw NDJSON must hold rows. An empty asset means the
    landing-page file discovery broke (URL pattern changed) or the WAF started
    blocking despite the browser UA."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 rows"


def test_fiscal_year_present_and_multiyear(spec_ids):
    """Each program should span several fiscal years (these are multi-year
    snapshots). If a program collapses to one year, file discovery likely
    matched only the latest file."""
    single = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        years = {r.get("fiscal_year") for r in rows if r.get("fiscal_year") is not None}
        assert years, f"{sid}: no fiscal_year on any row"
        if len(years) < 2:
            single.append((sid, sorted(years)))
    assert not single, f"programs with only one fiscal year (expected multi-year): {single}"


def test_rows_have_multiple_columns(spec_ids):
    """A degenerate parse (wrong header row) often yields 1-2 columns. Real HUD
    tables are wide (geo identifiers + several metrics)."""
    thin = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows:
            ncols = max(len(r) for r in rows[:200])
            if ncols < 4:
                thin.append((sid, ncols))
    assert not thin, f"programs whose rows have <4 columns (bad header row?): {thin}"
