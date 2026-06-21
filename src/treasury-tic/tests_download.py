"""Health invariants for Treasury TIC raw downloads.

Run post-DAG in-connector; loads raw through the same loader the download used.
Catches silent degradation: empty/truncated files, format drift, lost columns.
"""
from subsets_utils import load_raw_parquet

MFH_ID = "treasury-tic-mfh-treasury-holdings"
SLT_IDS = [
    "treasury-tic-slt1-us-lt-securities-held-by-foreign-residents",
    "treasury-tic-slt2-foreign-lt-securities-held-by-us-residents",
    "treasury-tic-slt3-us-treasury-securities-held-by-foreign-residents",
    "treasury-tic-slt4-us-purchases-sales-lt-securities-by-type",
]


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must persist a non-empty raw parquet."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_mfh_shape():
    """MFH is the deep historical series — expect thousands of country-months
    back to the 20th century, with non-null holdings."""
    t = load_raw_parquet(MFH_ID)
    cols = set(t.column_names)
    assert {"country", "date", "holdings_billions"} <= cols, f"MFH cols={cols}"
    assert t.num_rows >= 5000, f"MFH only {t.num_rows} rows; expected >=5000"
    dates = t.column("date").to_pylist()
    assert min(dates) <= "1999-12", f"MFH earliest date {min(dates)} too recent"
    assert max(dates) >= "2024-01", f"MFH latest date {max(dates)} stale"
    hb = t.column("holdings_billions").to_pylist()
    assert all(v is not None for v in hb), "MFH has null holdings"
    n_countries = len(set(t.column("country").to_pylist()))
    assert n_countries >= 30, f"MFH only {n_countries} countries; expected >=30"


def test_slt_shape():
    """Each SLT detailed table is long-format with country_code + monthly dates
    across ~90+ countries; guard against the parser capping after the banner."""
    for sid in SLT_IDS:
        t = load_raw_parquet(sid)
        cols = set(t.column_names)
        assert {"country", "country_code", "date"} <= cols, f"{sid} cols={cols}"
        assert len(cols) >= 6, f"{sid}: only {len(cols)} columns"
        assert t.num_rows >= 1000, f"{sid}: only {t.num_rows} rows; expected >=1000"
        dates = t.column("date").to_pylist()
        assert max(dates) >= "2024-01", f"{sid}: latest date {max(dates)} stale"
        n_countries = len(set(t.column("country").to_pylist()))
        assert n_countries >= 40, f"{sid}: only {n_countries} countries"
