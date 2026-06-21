"""Health-invariant tests for the INE Chile connector.

Each download node saves its dataflow as a verbatim SDMX-CSV raw asset via
save_raw_file(..., extension="csv"). These tests load it back with the same
loader and catch silent degradation: empty payloads, header-only responses,
or a format switch away from comma-delimited CSV.
"""

from subsets_utils import load_raw_file


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow returned data when probed; a header-only or empty CSV
    means the SDMX data endpoint changed format or started erroring silently."""
    bad = []
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        # header + at least one observation row
        if len(lines) < 2:
            bad.append((sid, len(lines)))
    assert not bad, f"{len(bad)} assets have no data rows: {bad[:10]}"


def test_csv_has_expected_columns(spec_ids):
    """SDMX-CSV from this instance always carries DATAFLOW, TIME_PERIOD and
    OBS_VALUE in the header (dimension columns vary per DSD). Missing any of
    these means the response is not the expected SDMX-CSV shape."""
    required = {"DATAFLOW", "TIME_PERIOD", "OBS_VALUE"}
    bad = []
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        header = text.splitlines()[0] if text else ""
        cols = {c.strip().strip('"') for c in header.split(",")}
        missing = required - cols
        if missing:
            bad.append((sid, sorted(missing)))
    assert not bad, f"{len(bad)} assets missing required columns: {bad[:10]}"
