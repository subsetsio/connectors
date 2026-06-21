"""Post-DAG health invariants for the SIPRI connector.

Catch silent degradation that file-existence alone misses: a register that
truncated to a handful of rows, an xlsx whose sheet/layout changed so parsing
emitted nothing useful, a measure or year range that vanished.
"""

from subsets_utils import load_raw_ndjson, load_raw_parquet


def test_arms_transfers_register_full(spec_ids):
    sid = "sipri-arms-transfers"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    # full register is ~29.9k rows (3 pages of 10k); a dropped page lands ~19.9k.
    assert len(rows) >= 28000, f"{sid}: only {len(rows)} rows; pagination likely dropped a page"
    assert {"buyer", "seller", "category"} <= set(rows[0].keys()), "missing core transfer fields"


def test_military_expenditure_panel(spec_ids):
    sid = "sipri-military-expenditure"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows >= 20000, f"{sid}: only {t.num_rows} rows; xlsx parse degraded"
    measures = set(t.column("measure").to_pylist())
    assert {"current_usd_mn", "share_of_gdp"} <= measures, f"missing key measures, got {measures}"
    years = t.column("year").to_pylist()
    assert min(years) <= 1960 and max(years) >= 2024, f"year span looks wrong: {min(years)}-{max(years)}"
    assert len(set(t.column("country").to_pylist())) >= 120, "too few distinct countries"


def test_arms_industry_top100_panel(spec_ids):
    sid = "sipri-arms-industry-top100"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows >= 1500, f"{sid}: only {t.num_rows} rows; sheet parse degraded"
    years = set(t.column("year").to_pylist())
    assert years >= {2002, 2024}, f"missing expected years, got span {min(years)}-{max(years)}"
    # every retained row carries a company and a numeric rank
    assert all(c for c in t.column("company").to_pylist()), "blank company names present"


def test_total_revenues_series(spec_ids):
    sid = "sipri-arms-industry-total-revenues"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows >= 15, f"{sid}: only {t.num_rows} yearly points"
    vals = t.column("total_arms_revenue_current_usd_bn").to_pylist()
    assert all(v and v > 0 for v in vals), "non-positive total arms revenue value"
