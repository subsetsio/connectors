"""Health-invariant tests for the SEEK connector raw assets."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. An empty payload usually
    means the discovery page changed, the CDN link rotated to a 404, or the
    XLSX sheet name moved."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns_present(spec_ids):
    """Each raw asset must carry date + state; the salary asset also carries
    classification. Missing columns mean a header/sheet drift slipped past the
    parser."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert {"date", "country", "state"} <= cols, f"{sid}: missing core columns ({cols})"
        if sid == "seek-advertised-salary-index":
            assert "classification" in cols, f"{sid}: missing classification column"
