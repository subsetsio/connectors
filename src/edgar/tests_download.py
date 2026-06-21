from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The unpivoted EDGAR table should hold hundreds of thousands of rows
    (4 substances x ~200 countries x ~25 sectors x ~50 years). A tiny count
    means a workbook failed to parse or the FTP returned an error page."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 100_000, f"{sid}: only {len(table)} rows"


def test_expected_gases_present(spec_ids):
    """All four CC BY 4.0 substance families must be represented; the IEA
    fossil-CO2 series must NOT be (license exclusion)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        gases = set(table.column("gas").to_pylist())
        for required in ("CH4", "N2O", "CO2bio"):
            assert required in gases, f"{sid}: missing gas {required}"
        # F-gases resolve into individual species — expect several.
        assert any(g and g.startswith("HFC-") for g in gases), \
            f"{sid}: no HFC species found (F-gases workbook failed?)"
        assert "CO2" not in gases, \
            f"{sid}: fossil CO2 present — IEA CC BY-NC-ND data leaked in"


def test_year_range(spec_ids):
    """Years should span the EDGAR coverage window (1970 onward)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = table.column("year").to_pylist()
        assert min(years) <= 1971, f"{sid}: earliest year {min(years)}"
        assert max(years) >= 2022, f"{sid}: latest year {max(years)}"
