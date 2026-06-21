"""Health-invariant tests for the Electoral Integrity Project connector.

Run post-DAG, in-connector. They load raw assets through subsets_utils and
catch silent degradation (empty/truncated downloads, lost score columns).
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Both PEI tables must hold rows; an empty payload means the Data Access
    API switched format or the .tab resolution broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_core_columns_present(spec_ids):
    """The PEI tables are wide (270+ columns); guard the identity + headline
    integrity-score columns that define the dataset's value."""
    needed = {"election", "country", "ISO", "year", "OVERALLINTEGRITY"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = needed - cols
        assert not missing, f"{sid}: missing core columns {missing}"


def test_election_table_reasonable_size(spec_ids):
    """The cumulative election-level table covers 600+ national contests;
    far fewer means a truncated download or wrong file resolved."""
    sid = "electoral-integrity-project-pei-election"
    if sid in spec_ids:
        n = len(load_raw_parquet(sid))
        assert n >= 300, f"{sid}: only {n} rows; expected 300+ contests"


def test_overallintegrity_in_range(spec_ids):
    """The PEI index is a 0-100 score; values outside that band signal a
    parse/column-shift error."""
    import pyarrow.compute as pc

    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "OVERALLINTEGRITY" not in table.column_names:
            continue
        col = pc.cast(table["OVERALLINTEGRITY"], "float64")
        vals = col.drop_null()
        if len(vals) == 0:
            continue
        lo = pc.min(vals).as_py()
        hi = pc.max(vals).as_py()
        assert 0 <= lo and hi <= 100, f"{sid}: OVERALLINTEGRITY out of [0,100]: [{lo},{hi}]"
