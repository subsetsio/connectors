"""Health-invariant tests for the Big Mac Index raw download."""

from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The single raw asset should hold a few thousand rows. A near-empty
    payload means GitHub served an error page or the CSV moved."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 1000, f"{sid}: raw parquet has {len(table)} rows (<1000)"


def test_schema_and_coverage(spec_ids):
    """Key columns present and populated; historical + recent spans both there."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        for required in ("date", "iso_a3", "dollar_price"):
            assert required in cols, f"{sid}: missing column {required!r}"

        dates = [d for d in table.column("date").to_pylist() if d]
        assert min(dates) < "2005-01-01", f"{sid}: no historical data, earliest {min(dates)}"
        assert max(dates) > "2020-01-01", f"{sid}: no recent data, latest {max(dates)}"

        countries = {c for c in table.column("iso_a3").to_pylist() if c}
        assert len(countries) >= 20, f"{sid}: only {len(countries)} countries (<20)"

        prices = [p for p in table.column("dollar_price").to_pylist() if p is not None]
        assert prices, f"{sid}: dollar_price all null"
        assert 0.5 < min(prices) and max(prices) < 25, (
            f"{sid}: dollar_price out of range [{min(prices)}, {max(prices)}]"
        )
