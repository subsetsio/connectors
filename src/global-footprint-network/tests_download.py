from subsets_utils import load_raw_parquet


def test_values_nonempty(spec_ids):
    """The raw pull should hold tens of thousands of rows (8 record types x
    ~200 countries x ~64 years). A near-empty payload means the Origin
    side-door access broke or the endpoint changed format."""
    table = load_raw_parquet("global-footprint-network-values")
    assert len(table) > 20000, f"values: only {len(table)} rows; expected >20000"


def test_values_record_types(spec_ids):
    """All 8 record types should be present; a missing type means a per-type
    bulk request silently returned nothing."""
    table = load_raw_parquet("global-footprint-network-values")
    records = set(table.column("record").to_pylist())
    expected = {
        "BiocapPerCap", "BiocapTotGHA", "EFConsPerCap", "EFConsTotGHA",
        "GDP", "HDI", "Population",
    }
    missing = expected - records
    assert not missing, f"missing record types in raw: {missing}"


def test_values_year_span(spec_ids):
    """Accounts run 1961-present; a collapsed span means a degraded pull."""
    table = load_raw_parquet("global-footprint-network-values")
    years = table.column("year").to_pylist()
    assert min(years) == 1961, f"min year {min(years)}; expected 1961"
    assert max(years) >= 2022, f"max year {max(years)}; expected >=2022"
