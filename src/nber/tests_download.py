"""Health invariants for the NBER raw assets. Run post-DAG, in-connector, via
the same subsets_utils loaders the download nodes wrote with."""
from subsets_utils import load_raw_parquet


def test_macrohistory_values_substantial():
    """The long-format observations across ~3500 series should be in the
    hundreds-of-thousands of rows. A tiny count means chapter enumeration or
    .dat parsing silently broke."""
    t = load_raw_parquet("nber-macrohistory-values")
    assert t.num_rows >= 200_000, f"only {t.num_rows} observation rows"
    cols = set(t.column_names)
    assert {"series_id", "date", "value", "frequency", "chapter"} <= cols, cols
    # values column must carry real, non-sentinel floats
    vals = [v for v in t.column("value").to_pylist() if v is not None]
    assert vals, "no non-null values"
    assert all(abs(v) < 1e30 for v in vals[:10000]), "missing-data sentinel leaked through"
    freqs = set(t.column("frequency").to_pylist()[:50000])
    assert freqs <= {"annual", "monthly", "quarterly"}, freqs


def test_macrohistory_series_catalog():
    """One catalog row per series (~3500), and most should carry a parsed
    title — a near-empty title column means the docs parser stopped matching."""
    t = load_raw_parquet("nber-macrohistory-series")
    assert t.num_rows >= 3000, f"only {t.num_rows} series in catalog"
    titles = [x for x in t.column("title").to_pylist() if x]
    assert len(titles) >= 0.5 * t.num_rows, (
        f"only {len(titles)}/{t.num_rows} series have a parsed title"
    )


def test_business_cycles_present():
    """~35 cycles, each with a trough date; the canonical chronology should not
    shrink to a handful."""
    t = load_raw_parquet("nber-business-cycle-dates")
    assert t.num_rows >= 30, f"only {t.num_rows} cycles"
    troughs = [x for x in t.column("trough").to_pylist() if x]
    assert len(troughs) >= 30, f"only {len(troughs)} troughs populated"
