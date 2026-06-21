"""Health-invariant tests for the DfE connector, run post-DAG in-connector.

Raw assets are all-VARCHAR Parquet written by the download node, so we load
them with the parquet reader and assert they carry rows and look like the EES
tabular shape rather than an error page or empty payload.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every data set's raw asset must hold rows. An empty payload usually means
    the CSV endpoint returned an error envelope or the dataset was withdrawn."""
    empty = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:5]}"


def test_has_columns(spec_ids):
    """Each asset must have at least a couple of columns; a single-column table
    would mean the CSV header parse collapsed."""
    bad = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_columns < 2:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have <2 columns: {bad[:5]}"


def test_has_time_period_column(spec_ids):
    """EES data set CSVs are statistical tables keyed on time_period. If almost
    none expose it, the endpoint format changed or we fetched the wrong thing."""
    with_tp = 0
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "time_period" in table.column_names:
            with_tp += 1
    assert with_tp >= len(spec_ids) * 0.8, (
        f"only {with_tp}/{len(spec_ids)} assets have a time_period column"
    )
