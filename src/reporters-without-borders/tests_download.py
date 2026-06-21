"""Health invariants for the RSF World Press Freedom Index raw download.

These run post-DAG, in-connector, against the raw parquet through the same
subsets_utils loader the fetch fn wrote with — catching silent degradation
(truncated download, an era dropped, the score column shifting) that mere file
existence would miss.
"""

from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The single index asset must hold thousands of country-year rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 3000, f"{sid}: only {len(table)} rows; expected >=3000 country-years"


def test_both_methodology_eras_present(spec_ids):
    """We must span both the pre-2022 and 2022+ methodology layouts; losing one
    means header detection or year discovery regressed."""
    for sid in spec_ids:
        eras = set(load_raw_parquet(sid).column("methodology_era").to_pylist())
        assert "old_pre2022" in eras, f"{sid}: no pre-2022 rows; eras={eras}"
        assert "new_2022" in eras, f"{sid}: no 2022+ rows; eras={eras}"


def test_year_coverage(spec_ids):
    """The latest index (2026) and a broad historical span must be present."""
    for sid in spec_ids:
        years = set(load_raw_parquet(sid).column("year").to_pylist())
        years.discard(None)
        assert len(years) >= 20, f"{sid}: only {len(years)} distinct years"
        assert max(years) >= 2026, f"{sid}: latest year is {max(years)}, expected >=2026"
        assert 2011 not in years, f"{sid}: 2011 present, but RSF published no 2011 index"


def test_subindicators_only_new_era(spec_ids):
    """Sub-indicator scores exist only from 2022 on; any pre-2022 row carrying a
    Safety score means an era was mislabelled."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        old = t.filter(pc.equal(t.column("methodology_era"), "old_pre2022"))
        bad = old.filter(pc.is_valid(old.column("safety")))
        assert len(bad) == 0, f"{sid}: {len(bad)} pre-2022 rows have a Safety sub-score"
        new = t.filter(pc.equal(t.column("methodology_era"), "new_2022"))
        scored = new.filter(pc.is_valid(new.column("safety")))
        assert len(scored) > 0, f"{sid}: no 2022+ rows carry sub-indicator scores"
