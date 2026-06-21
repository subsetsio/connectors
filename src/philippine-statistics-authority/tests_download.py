"""Post-DAG health invariants for the PSA OpenSTAT connector.

Catches silent degradation that per-spec expectation files miss — wholesale
empty pulls or a value column that lost its numeric type across the catalog.
Loads raw through the same loader the download node wrote with.
"""

import pyarrow as pa
from subsets_utils import load_raw_parquet


def _sample(spec_ids, k=40):
    """Deterministic, evenly-spread sample so the check stays cheap on a
    3000-table catalog while still touching every region of the id space."""
    ids = sorted(spec_ids)
    if len(ids) <= k:
        return ids
    step = len(ids) / k
    return [ids[int(i * step)] for i in range(k)]


def test_sampled_assets_nonempty_and_numeric(spec_ids):
    """Every sampled table's raw parquet must hold rows and expose a numeric
    `value` column. Empty payloads or a non-float `value` mean the PXWeb
    json-stat2 decode silently broke."""
    for sid in _sample(spec_ids):
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"
        assert "value" in table.column_names, f"{sid}: missing 'value' column"
        assert pa.types.is_floating(table.schema.field("value").type), \
            f"{sid}: 'value' is {table.schema.field('value').type}, expected float"


def test_some_observations_present(spec_ids):
    """Across the sample, at least some non-null observations exist — a catalog
    where every table is all-null would publish nothing downstream and signals
    a systemic decode/selection failure rather than a few genuinely sparse
    tables."""
    seen_nonnull = 0
    for sid in _sample(spec_ids):
        table = load_raw_parquet(sid)
        if table.num_rows and table.column("value").null_count < table.num_rows:
            seen_nonnull += 1
    assert seen_nonnull > 0, "no non-null observations across sampled tables"
