"""Post-DAG health invariants for the eurobarometer connector.

Run in-connector after the fetches, through subsets_utils loaders — so they see
the data identically local or in the cloud. They catch silent degradation that
file-existence checks miss: empty payloads, truncated downloads, a parser that
went quiet.
"""
from subsets_utils import load_raw_parquet, list_raw_files


def test_surveys_nonempty():
    """The survey catalog should hold one row per COMMU dataset (~1000)."""
    table = load_raw_parquet("eurobarometer-surveys")
    assert table.num_rows > 100, f"surveys: only {table.num_rows} rows"
    assert {"survey_id", "title", "num_distributions"} <= set(table.column_names)


def test_responses_batches_nonempty():
    """At least one Volume-A workbook must parse to response rows, and the
    parsed shares must be valid proportions."""
    rels = list_raw_files("eurobarometer-responses-*.parquet")
    assert rels, "no eurobarometer-responses batch parquet files were written"

    total = 0
    checked_shares = False
    for rel in rels[:25]:  # sample — the full set can be hundreds of batches
        asset_id = rel[:-len(".parquet")]
        table = load_raw_parquet(asset_id)
        total += table.num_rows
        if not checked_shares and "share" in table.column_names and table.num_rows:
            shares = [s for s in table.column("share").to_pylist() if s is not None]
            assert all(0.0 <= s <= 1.0 for s in shares), \
                f"{asset_id}: share values outside [0,1]"
            checked_shares = True
    assert total > 0, "responses batches exist but hold 0 rows"
