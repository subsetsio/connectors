"""In-connector health invariants for the BNR exchange-rate download.

Run post-DAG via subsets_utils loaders, so they behave identically locally and
in the cloud. These catch silent degradation that file-existence alone misses:
an empty payload, a collapsed currency set, or a missing rate column.
"""

from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    expected = {"currency_name", "buying_rate", "average_rate", "selling_rate", "post_date"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert expected <= cols, f"{sid}: missing columns {expected - cols}"


def test_many_currencies(spec_ids):
    """The corpus should span many currencies — a single-currency pull means the
    enumeration broke after the first code."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        distinct = set(table.column("currency_name").to_pylist())
        assert len(distinct) >= 30, f"{sid}: only {len(distinct)} currencies; expected >=30"
