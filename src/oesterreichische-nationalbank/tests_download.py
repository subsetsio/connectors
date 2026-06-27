"""Health invariants for the OeNB connector, run post-DAG in-connector.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, the values batch layout going missing.
"""

from subsets_utils import list_raw_files, load_raw_parquet

SLUG = "oesterreichische-nationalbank"


def test_positions_nonempty():
    """The positions catalog must hold rows; an empty one means the content
    tree walk silently returned nothing (format change / auth break)."""
    table = load_raw_parquet(f"{SLUG}-positions")
    assert len(table) > 0, "positions raw parquet has 0 rows"


def test_values_batches_present_and_nonempty():
    """values is written as one parquet batch per category node
    (<asset>-<hierid>.parquet). At least several node batches must exist and
    together carry observations."""
    files = list_raw_files(f"{SLUG}-values-*.parquet")
    assert len(files) >= 5, f"expected several values node batches, got {files}"
    total = 0
    for rel in files:
        asset_id = rel.rsplit("/", 1)[-1][: -len(".parquet")]
        total += len(load_raw_parquet(asset_id))
    assert total > 0, "values batches present but hold 0 observations total"
