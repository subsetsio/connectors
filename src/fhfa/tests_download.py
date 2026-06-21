"""Post-DAG health invariants for the FHFA connector.

These run in-connector after the download nodes, loading raw the same way the
nodes saved it (parquet). They catch silent degradation that file-existence
alone misses: a switched endpoint returning an empty/HTML payload, a truncated
download, a format change that drops the expected columns.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "fhfa-hpi": {"hpi_type", "hpi_flavor", "place_id", "yr", "period", "index_nsa"},
    "fhfa-conforming-loan-limits": {"year", "fips_state_code", "county_name", "one_unit_limit"},
    "fhfa-mirs-transition-index": {"release_date", "index_value"},
    "fhfa-nmdb-aggregate-statistics": {"seriesid", "year", "value1"},
    "fhfa-uad-aggregate-statistics": {"seriesid", "geolevel", "year", "value"},
    "fhfa-pudb-enterprise-single-family": {"enterprise", "record_num_sf_nfb", "purpose_sf_nfb"},
    "fhfa-pudb-enterprise-multifamily": {"enterprise", "record_num_mf_nf", "purpose_mf_nf"},
    "fhfa-pudb-fhlbank": {"Year", "Bank", "LoanAcquisitionActualUPBAmt"},
    "fhfa-enterprise-housing-goals": {"state", "year", "metric", "value"},
}

# Loose floors — tight enough that a truncated/empty payload trips them, loose
# enough to survive normal release-to-release fluctuation.
MIN_ROWS = {
    "fhfa-hpi": 100_000,
    "fhfa-conforming-loan-limits": 3_000,      # ~3200 counties x >=1 year
    "fhfa-mirs-transition-index": 24,          # monthly since 2019
    "fhfa-nmdb-aggregate-statistics": 100_000,
    "fhfa-uad-aggregate-statistics": 100_000,
    "fhfa-pudb-enterprise-single-family": 500_000,
    "fhfa-pudb-enterprise-multifamily": 100,
    "fhfa-pudb-fhlbank": 10_000,
    "fhfa-enterprise-housing-goals": 100,      # ~50 states x metrics x years
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet must hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    """The columns each transform depends on must exist in raw — a silent
    format change (renamed/dropped header) would otherwise surface only as an
    empty published table much later."""
    for sid in spec_ids:
        expected = EXPECTED_COLUMNS.get(sid)
        if not expected:
            continue
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing expected columns {missing} (have {sorted(cols)[:8]}...)"


def test_min_rows(spec_ids):
    """Row-count floors catch truncated downloads (e.g. an HTML error page
    parsed as a 1-row CSV)."""
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = load_raw_parquet(sid).num_rows
        assert n >= floor, f"{sid}: {n} rows < expected floor {floor}"
