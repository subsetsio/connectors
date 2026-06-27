"""Health-invariant tests for the Maven Central connector. Run post-DAG,
in-connector, so loaders resolve identically local or on GitHub Actions."""
from subsets_utils import load_raw_parquet


def test_artifacts_nonempty(spec_ids):
    """The raw artifact catalog must hold a large number of rows. An empty or
    tiny payload means the Solr endpoint switched format, throttled us out, or
    pagination broke after page one."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 400000, f"{sid}: raw parquet has only {len(table)} rows; expected the full ~662k catalog"


def test_coordinates_present(spec_ids):
    """group_id and artifact_id must be fully populated — they are the natural
    key of the catalog."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        for col in ("group_id", "artifact_id"):
            nulls = table.column(col).null_count
            assert nulls == 0, f"{sid}: {nulls} null values in {col}"
