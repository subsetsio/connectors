"""Health-invariant tests for the BCP cotizacion raw assets.

These run post-DAG, in-connector, and load raw through the same loader the
download nodes used (save_raw_parquet -> load_raw_parquet). They catch silent
degradation that file-existence alone misses: an empty scrape (site moved /
markup changed), or a parser that stopped matching the number format."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every node must land rows. A 0-row parquet means the cotizacion markup
    changed or the Spanish-locale number regex stopped matching."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_monthly_has_many_currencies(spec_ids):
    """The monthly planilla lists ~23 currencies; if we see <10 the per-row
    currency-code filter is over-rejecting or only one month parsed."""
    sid = "banco-central-del-paraguay-monthly-currency-reference-rates"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    codes = set(table.column("currency_code").to_pylist())
    assert len(codes) >= 10, f"{sid}: only {len(codes)} distinct currencies: {sorted(codes)}"


def test_daily_rates_positive(spec_ids):
    """Guarani-per-USD rates are always positive and in a sane band; a zero or
    absurd value means a column got mis-parsed (e.g. units vs guaranies)."""
    sid = "banco-central-del-paraguay-daily-usd-reference-rate"
    if sid not in spec_ids:
        return
    vals = [v for v in load_raw_parquet(sid).column("guaranies_per_usd").to_pylist() if v is not None]
    assert vals, f"{sid}: no non-null rates"
    assert min(vals) > 100 and max(vals) < 100000, (
        f"{sid}: rate range looks wrong: min={min(vals)} max={max(vals)}"
    )
