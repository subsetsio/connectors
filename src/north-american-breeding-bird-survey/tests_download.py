"""Health-invariant tests for the BBS connector raw assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
nodes used to write. Catch silent degradation that file-existence alone misses:
empty payloads, truncated zip streams, a source that switched format.
"""

from subsets_utils import load_raw_parquet

SLUG = "north-american-breeding-bird-survey"


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet must hold rows. Empty usually means the
    ScienceBase file moved/renamed and the predicate matched nothing useful, or a
    truncated download."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_count_tables_are_large(spec_ids):
    """The two count tables span 1966-present across thousands of routes and
    ~700 taxa — they must be in the millions of rows. A tiny count means the zip
    only unpacked one member (stream broke) or a single chunk was written."""
    for name, floor in (("state-counts", 1_000_000), ("fifty-stop-counts", 500_000)):
        sid = f"{SLUG}-{name}"
        if sid in spec_ids:
            n = len(load_raw_parquet(sid))
            assert n >= floor, f"{sid}: only {n} rows (expected >= {floor})"


def test_key_columns_present(spec_ids):
    """AOU (species code) and Year anchor the count/index tables; their absence
    means the header row was consumed as data or columns were renamed upstream."""
    expect = {
        f"{SLUG}-state-counts": ["AOU", "Year", "RouteDataID"],
        f"{SLUG}-fifty-stop-counts": ["AOU", "Year", "Stop1", "Stop50"],
        f"{SLUG}-analysis-core-indices": ["AOU", "Region", "Year", "Index"],
        f"{SLUG}-species-list": ["AOU", "English_Common_Name"],
    }
    for sid, cols in expect.items():
        if sid in spec_ids:
            have = set(load_raw_parquet(sid).column_names)
            missing = [c for c in cols if c not in have]
            assert not missing, f"{sid}: missing columns {missing} (have {sorted(have)})"
