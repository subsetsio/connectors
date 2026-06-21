"""Health-invariant tests for the CCEI connector raw assets.

Each download node saves the dataflow's full SDMX-CSV verbatim via
save_raw_file(..., extension="csv"). These tests catch silent degradation
(empty payloads, truncated downloads, format switch) that file existence misses.
"""

from subsets_utils import load_raw_file


def test_all_raw_assets_nonempty(spec_ids):
    """Every flow's raw CSV should hold a header plus at least one data row.
    A header-only (or empty) file usually means the endpoint switched format,
    returned XML instead of CSV, or the flow went inactive."""
    bad = []
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        if len(lines) < 2:
            bad.append(sid)
    assert not bad, f"{len(bad)} raw CSV assets have no data rows: {bad[:10]}"


def test_raw_assets_are_csv_not_xml(spec_ids):
    """The server ignores ?format=text/csv and returns SDMX-XML unless the
    Accept header is honored; guard against a silent revert to XML."""
    bad = []
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        head = text.lstrip()[:64].lower()
        if head.startswith("<?xml") or head.startswith("<message"):
            bad.append(sid)
    assert not bad, f"{len(bad)} raw assets are XML, not CSV: {bad[:10]}"


def test_raw_csv_has_obs_value_column(spec_ids):
    """Every SDMX-CSV data response carries DATAFLOW, TIME_PERIOD and OBS_VALUE
    in its header; a missing OBS_VALUE means the transform will publish nothing."""
    bad = []
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        header = text.splitlines()[0] if text.strip() else ""
        cols = {c.strip() for c in header.split(",")}
        if not {"OBS_VALUE", "TIME_PERIOD"}.issubset(cols):
            bad.append(sid)
    assert not bad, f"{len(bad)} raw CSVs missing OBS_VALUE/TIME_PERIOD: {bad[:10]}"
