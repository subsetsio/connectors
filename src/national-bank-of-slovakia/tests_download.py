"""Post-DAG health invariants for the NBS exchange-rate connector (foreign feed).

The foreign feed is written as a single parquet asset per its download spec."""

from subsets_utils import load_raw_parquet


def test_foreign_raw_nonempty(spec_ids):
    """The monthly foreign feed must hold rows. An empty payload means the WAF
    blocked us, the endpoint changed shape, or parsing dropped everything."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_foreign_columns(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert {"valid_from", "country", "currency_code", "currency_name", "value"} <= cols, (
            f"{sid}: unexpected columns {cols}"
        )


def test_foreign_currency_breadth(spec_ids):
    """Each month quotes ~130-150 currencies; across all history we expect well
    over 100 distinct codes. Far fewer means the walk was truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        distinct = len(set(table.column("currency_code").to_pylist()))
        assert distinct >= 100, f"{sid}: only {distinct} distinct currency codes"
