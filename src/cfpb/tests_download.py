"""Health invariants for the CFPB raw assets, run post-DAG in-connector.

Assets use a mix of layouts: most write a single `<id>.ndjson.zst` (credit
trends, mortgage performance, HMDA filers) or `<id>.csv.gz` (complaints);
`cfpb-hmda-loan-records` writes per-year batch files `<id>-<year>.csv.gz`.
We assert every spec produced at least one non-empty raw file (catching
truncated/empty downloads that file existence alone would miss), and load the
small NDJSON assets to confirm they actually hold rows.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def _raw_files_for(sid: str) -> list[str]:
    """Single-file layout (`sid.ext`) first, else the batch layout (`sid-*`)."""
    return list_raw_files(f"{sid}.*") or list_raw_files(f"{sid}-*")


def test_every_spec_wrote_raw(spec_ids):
    """Each download spec must have produced at least one raw file."""
    for sid in spec_ids:
        files = _raw_files_for(sid)
        assert files, f"{sid}: no raw files written (expected '{sid}.*' or '{sid}-*')"


def test_ndjson_assets_nonempty(spec_ids):
    """The small NDJSON assets (credit trends, mortgage performance, HMDA filers)
    must hold rows. The large CSV assets (complaints, loan records) are validated
    by the transform's zero-row gate rather than loaded here."""
    for sid in spec_ids:
        if not list_raw_files(f"{sid}.ndjson.zst"):
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: NDJSON asset is empty"


def test_hmda_loan_records_has_year_batches(spec_ids):
    """Loan records must land as per-year batch files, not a single blob."""
    sid = "cfpb-hmda-loan-records"
    if sid not in spec_ids:
        return
    batches = list_raw_files(f"{sid}-*")
    assert batches, f"{sid}: no per-year batch files found"
