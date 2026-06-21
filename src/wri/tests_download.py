"""Health-invariant tests for the WRI (Climate Watch) connector raw assets.

These run post-DAG against the data the download nodes wrote, via the same
subsets_utils loaders. They catch silent degradation: an export that switched
format, an auth wall, a truncated ZIP that yields a near-empty table.
"""

from subsets_utils import load_raw_parquet


def test_all_assets_nonempty(spec_ids):
    """Every download asset must hold rows. Empty usually means the bulk
    export changed shape or returned an error page instead of a ZIP."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_emissions_shape():
    """historical_emissions is the flagship: it must unpivot into a large long
    table spanning a wide year range and carrying real (non-zero) values."""
    t = load_raw_parquet("wri-historical-emissions")
    assert len(t) > 500_000, f"emissions long rows={len(t)}, expected >500k"
    years = t.column("year").to_pylist()
    assert min(years) <= 1900, f"earliest year {min(years)} too late"
    assert max(years) >= 2020, f"latest year {max(years)} too early"
    # The series is mostly placeholder zeros; ensure real signal survived.
    vals = t.column("value").to_pylist()
    assert any(v and v > 0 for v in vals), "no positive emission values present"
    isos = set(t.column("iso_code3").to_pylist())
    assert len(isos) > 100, f"only {len(isos)} distinct ISO codes"


def test_content_columns():
    """NDC/net-zero content tables must keep their indicator columns populated."""
    for sid in ("wri-ndc-content", "wri-net-zero-content"):
        t = load_raw_parquet(sid)
        assert "indicator_id" in t.column_names, f"{sid}: missing indicator_id"
        ind = [x for x in t.column("indicator_id").to_pylist() if x]
        assert ind, f"{sid}: all indicator_id values are null/empty"
        countries = set(t.column("iso_code3").to_pylist())
        assert len(countries) > 20, f"{sid}: only {len(countries)} countries"
