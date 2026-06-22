"""Health invariants for the Cisco Umbrella popularity-list raw assets.

These catch silent degradation that file existence alone misses: a truncated
download, a format switch, or an empty payload after the endpoint changed.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet must hold rows. An empty payload
    usually means the ZIP/CSV format changed or the GET returned an error body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_rank_column_present(spec_ids):
    """Both feeds are (rank, name) tuples — the rank column must survive parsing.
    A missing rank means the headerless CSV was misparsed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "rank" in table.column_names, f"{sid}: missing 'rank' column ({table.column_names})"


def test_domains_full_million(spec_ids):
    """The domains feed is the top 1,000,000 — anything far short signals a
    truncated download or a partial unzip."""
    sid = "cisco-umbrella-top-1m-domains"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert len(table) >= 900000, f"{sid}: only {len(table)} rows, expected ~1,000,000"
