"""Health invariants for the Croatian National Bank raw downloads.

Both corpora are small and full-pulled each run via one wide date-range
request, so a large shortfall signals a truncated/altered endpoint rather
than normal growth. The kuna table is frozen (1994-2022); the euro table
grows by ~13 rows each business day.
"""

from subsets_utils import load_raw_parquet

# Floors observed at authoring time (mid-2026), set well below the true counts.
_MIN_ROWS = {
    "croatian-national-bank-exchange-rates-eur": 9000,
    "croatian-national-bank-exchange-rates-hrk": 80000,
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_row_counts(spec_ids):
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        table = load_raw_parquet(sid)
        assert len(table) >= floor, (
            f"{sid}: only {len(table)} rows, expected >= {floor} "
            "(possible truncated date-range pull)"
        )


def test_middle_rate_present(spec_ids):
    """The middle rate must be populated — it is the primary published value."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("srednji_tecaj")
        non_null = len(col) - col.null_count
        assert non_null > 0, f"{sid}: `srednji_tecaj` column is entirely null"


def test_major_currencies_covered(spec_ids):
    """USD/GBP/CHF have been quoted throughout; their absence means a bad pull."""
    expected = {"USD", "GBP", "CHF"}
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        present = set(table.column("valuta").to_pylist())
        missing = expected - present
        assert not missing, f"{sid}: missing major currencies {missing}"
