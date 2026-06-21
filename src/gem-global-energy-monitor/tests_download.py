"""Health invariants for the GEM connector's raw assets.

Each spec writes one NDJSON workbook-sheet dump. We check every asset loaded
back holds rows and a plausibly-wide schema (a truncated download or a switch
to the wrong sheet would collapse the column count), and that the flagship
integrated-power tracker carries its expected unit-level volume.
"""

from subsets_utils import load_raw_ndjson

SLUG = "gem-global-energy-monitor"


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's NDJSON should hold rows; empty means the presign
    flow, the GET, or the sheet-pick silently failed."""
    empties = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empties.append(sid)
    assert not empties, f"raw assets with 0 rows: {empties}"


def test_schema_width_reasonable(spec_ids):
    """GEM primary registries are wide (>=8 columns). A narrow schema means we
    landed on a dictionary/pivot sheet instead of the data sheet."""
    narrow = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and len(rows[0]) < 8:
            narrow.append((sid, len(rows[0])))
    assert not narrow, f"assets with suspiciously narrow schema: {narrow}"


def test_integrated_power_volume(spec_ids):
    """The Integrated Power Tracker is a unit-level global registry (~180k
    rows). A sharp drop signals a partial download or wrong sheet."""
    sid = f"{SLUG}-integrated-power-tracker"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 50000, f"integrated-power has only {len(rows)} rows; expected >=50000"
