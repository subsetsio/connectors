from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_full(spec_ids):
    """The Majestic Million CSV is exactly the top 1M domains. A short table
    means a truncated download or a silently switched endpoint."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 990000, f"{sid}: only {len(table)} rows; expected ~1,000,000"


def test_expected_columns(spec_ids):
    """Guard against an upstream header change renaming/dropping columns."""
    expected = {
        "GlobalRank", "TldRank", "Domain", "TLD", "RefSubNets", "RefIPs",
        "IDN_Domain", "IDN_TLD", "PrevGlobalRank", "PrevTldRank",
        "PrevRefSubNets", "PrevRefIPs",
    }
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing expected columns {missing}"
