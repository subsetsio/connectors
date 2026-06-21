"""Health-invariant tests for the NCES (IPEDS) download stage.

Run post-DAG inside the connector. They load raw through subsets_utils loaders
(same as the download node wrote), so they behave identically local or in cloud.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

# Small components (few thousand institution-rows per year) safe to fully load in
# a test without OOM. Used for content checks; presence is checked across all.
_SMALL_SAMPLE = [
    "nces-ipeds-hd",
    "nces-ipeds-drvef",
    "nces-ipeds-al",
    "nces-ipeds-eap",
]


def test_every_asset_present(spec_ids):
    """Each download spec must have produced exactly one raw NDJSON file. A
    missing file means the component's whole year-scan came up empty (URL
    templating broke or the server changed layout)."""
    for sid in spec_ids:
        matches = list_raw_files(f"{sid}.*")
        assert matches, f"{sid}: no raw file written"
        assert len(matches) == 1, f"{sid}: expected 1 raw file, got {matches}"


def test_sample_assets_have_rows_and_keys(spec_ids):
    """Representative small components must hold rows keyed on UNITID + year.
    Catches silent format breakage (empty payload, wrong decode, lost columns)."""
    for sid in _SMALL_SAMPLE:
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"
        first = rows[0]
        assert "UNITID" in first, f"{sid}: missing UNITID key"
        assert "year" in first, f"{sid}: missing year key"


def test_sample_spans_multiple_years(spec_ids):
    """A core component (institutional directory) should cover many collection
    years — if only one year came back, the historical year scan silently
    stopped after the first hit."""
    sid = "nces-ipeds-hd"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    years = {r.get("year") for r in rows}
    assert len(years) >= 10, f"{sid}: only {len(years)} distinct years ({sorted(years)[:5]}...)"
