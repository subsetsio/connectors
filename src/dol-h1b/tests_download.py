"""Health invariants for the dol-h1b download stage.

Raw is written as one parquet batch per period under the asset id
`dol-h1b-h1b-lca-disclosures-<period>`, so we discover batches via
list_raw_files rather than loading a single fixed asset.
"""
from subsets_utils import list_raw_files, load_raw_parquet

EXPECTED_COLS = {
    "fiscal_year", "quarter", "case_status", "employer_name",
    "soc_code", "wage_rate", "worksite_state",
}


def _batch_ids():
    paths = list_raw_files("dol-h1b-h1b-lca-disclosures-*.parquet")
    # Strip directory + .parquet to recover asset ids.
    ids = []
    for p in paths:
        name = p.rsplit("/", 1)[-1]
        if name.endswith(".parquet"):
            ids.append(name[: -len(".parquet")])
    return ids


def test_periods_downloaded():
    """We expect dozens of period files. A near-empty set means Akamai blocked
    the run wholesale or the URL pattern broke — flag heavy degradation."""
    ids = _batch_ids()
    assert len(ids) >= 5, f"only {len(ids)} period batches downloaded: {ids}"


def test_batches_nonempty_and_typed():
    """Each batch must hold rows and carry the core schema; empty/mis-typed
    batches mean the xlsx parse silently degraded."""
    ids = _batch_ids()
    assert ids, "no period batches found"
    total = 0
    for sid in ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: 0 rows"
        missing = EXPECTED_COLS - set(table.column_names)
        assert not missing, f"{sid}: missing columns {missing}"
        total += table.num_rows
    assert total >= 100_000, f"only {total:,} rows across all periods"
