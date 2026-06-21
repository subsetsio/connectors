from subsets_utils import load_raw_parquet


def test_composite_indices_shape(spec_ids):
    """The HDR composite-indices long table should hold tens of thousands of
    observations across many indicators, countries and years. A near-empty
    or single-indicator result means the wide CSV changed shape or the unpivot
    broke."""
    t = load_raw_parquet("undp-composite-indices")
    assert t.num_rows >= 20000, f"composite-indices: only {t.num_rows} rows"
    cols = t.column_names
    assert {"iso3", "indicator", "year", "value"} <= set(cols)
    indicators = set(t.column("indicator").to_pylist())
    assert len(indicators) >= 20, f"only {len(indicators)} distinct indicators"
    assert "hdi" in indicators, "core indicator 'hdi' missing"
    years = t.column("year").to_pylist()
    assert min(years) <= 1990 and max(years) >= 2020, f"year span off: {min(years)}..{max(years)}"


def test_mpi_shape(spec_ids):
    """gMPI Table 1 lists ~100+ developing countries; far fewer means the
    fixed-position parse drifted or the sheet layout changed."""
    t = load_raw_parquet("undp-mpi")
    assert t.num_rows >= 80, f"mpi: only {t.num_rows} country rows"
    assert {"country", "survey", "mpi_value", "headcount_pct", "intensity_pct",
            "contrib_health_pct", "severe_poverty_pct"} <= set(t.column_names)
    mpi_vals = [v for v in t.column("mpi_value").to_pylist() if v is not None]
    assert mpi_vals, "mpi_value column entirely null"
    assert all(0.0 <= v <= 1.0 for v in mpi_vals), "MPI values must fall in [0,1]"
