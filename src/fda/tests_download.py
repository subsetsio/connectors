"""Post-DAG health invariants for the FDA connector.

Each download spec writes one parquet batch per manifest partition
(`<spec_id>-<idx>`), so we glob the batch files and load the first to confirm
the fetch actually produced typed, non-empty rows — empty payloads usually mean
the manifest shape changed or a partition download silently truncated.
"""

from subsets_utils import list_raw_files, load_raw_parquet


def test_every_spec_has_batches(spec_ids):
    for sid in spec_ids:
        batches = list_raw_files(f"{sid}-*.parquet")
        assert batches, f"{sid}: no parquet batch files written"


def test_first_batch_nonempty(spec_ids):
    for sid in spec_ids:
        batches = sorted(list_raw_files(f"{sid}-*.parquet"))
        assert batches, f"{sid}: no parquet batches to check"
        batch_id = batches[0][: -len(".parquet")]
        table = load_raw_parquet(batch_id)
        assert len(table) > 0, f"{sid}: first batch {batch_id} has 0 rows"
        assert table.num_columns > 0, f"{sid}: first batch has no columns"
