"""Health-invariant tests for the MHCLG connector, run post-DAG in-connector.

Catch silent degradation the file-existence check misses: empty extractions
(endpoint switched format / attachment list changed), or a parser change that
drops the uniform cell schema.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "attachment_filename", "attachment_title", "content_type", "sheet_name",
    "row_index", "col_index", "value", "value_numeric",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every publication exposes at least one parseable spreadsheet, so its
    cell extraction must hold rows. Zero rows means the Content API stopped
    returning tabular attachments or every parse failed silently."""
    empties = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0:
            empties.append(sid)
    assert not empties, f"{len(empties)} raw assets are empty: {empties[:5]}"


def test_schema_uniform(spec_ids):
    """The cell extraction schema is uniform across every publication; a drift
    means the writer schema changed and downstream SQL will break."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_some_numeric_values(spec_ids):
    """Statistical tables are mostly numbers; across the whole connector a
    meaningful fraction of cells must parse as numeric. All-null numeric would
    mean the numeric parser silently broke."""
    import pyarrow.compute as pc

    numeric = 0
    total = 0
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value_numeric")
        total += len(col)
        numeric += len(col) - col.null_count
    assert total > 0, "no cells extracted across the entire connector"
    frac = numeric / total
    assert frac > 0.1, f"only {frac:.1%} of cells parsed as numeric; parser likely broke"
