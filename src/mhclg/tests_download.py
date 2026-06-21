"""Health-invariant tests for the MHCLG connector, run post-DAG in-connector.

Catch silent degradation file-existence misses: empty extractions (Content API
stopped returning tabular attachments, or every parse failed), a dropped
schema, or a `cells` payload that is no longer a JSON array.
"""

import json

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "attachment_filename", "attachment_title", "content_type", "sheet_name",
    "row_index", "n_cols", "cells",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every publication exposes at least one parseable spreadsheet, so its row
    extraction must hold rows. Zero rows means the Content API stopped returning
    tabular attachments or every parse failed silently."""
    empties = [sid for sid in spec_ids if len(load_raw_parquet(sid)) == 0]
    assert not empties, f"{len(empties)} raw assets are empty: {empties[:5]}"


def test_schema_uniform(spec_ids):
    """The row-extraction schema is uniform across every publication; drift
    means the writer schema changed and the SQL transforms will break."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_cells_are_json_arrays(spec_ids):
    """`cells` must always decode to a JSON list whose length matches n_cols —
    that contract is what lets a consumer reconstruct the source tables."""
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        if len(t) == 0:
            continue
        head = t.slice(0, 50).to_pylist()
        for r in head:
            arr = json.loads(r["cells"])
            assert isinstance(arr, list), f"{sid}: cells is not a JSON list: {r['cells'][:80]}"
            assert len(arr) == r["n_cols"], f"{sid}: n_cols={r['n_cols']} but cells has {len(arr)}"
