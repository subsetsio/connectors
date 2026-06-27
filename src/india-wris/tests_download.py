"""Health invariants for India-WRIS raw assets.

Theme assets are written as one ndjson batch per state (asset ids
`india-wris-<theme>-<state>`), so we probe them via list_raw_files glob rather
than loading a single asset. The stations reference is a single asset.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def test_themes_have_state_batches(spec_ids):
    """Each observation theme should write at least one non-empty state batch.
    Zero batches means the theme's agency/module filter matched nothing — a
    silently wrong configuration, not a healthy empty result."""
    theme_ids = [s for s in spec_ids if s != "india-wris-stations"]
    missing = [sid for sid in theme_ids if not list_raw_files(f"{sid}-*")]
    assert not missing, f"themes with no state batches: {missing}"


def test_stations_nonempty(spec_ids):
    """The station registry must hold rows; empty means every station-master
    call returned nothing (endpoint/format drift or auth change)."""
    if "india-wris-stations" not in spec_ids:
        return
    rows = load_raw_ndjson("india-wris-stations")
    assert len(rows) > 0, "india-wris-stations: 0 rows"


def test_canonical_fields_present(spec_ids):
    """A sampled theme batch must carry the canonical observation keys; a
    missing key means the normalization contract silently broke."""
    expected = {"theme", "station_code", "latitude", "longitude",
                "observed_date", "value", "record"}
    for sid in spec_ids:
        if sid == "india-wris-stations":
            continue
        batches = list_raw_files(f"{sid}-*")
        if not batches:
            continue
        # asset id = filename without the compression/format suffix
        fname = batches[0].rsplit("/", 1)[-1]
        asset_id = fname.split(".")[0]
        rows = load_raw_ndjson(asset_id)
        if not rows:
            continue
        missing = expected - set(rows[0].keys())
        assert not missing, f"{asset_id}: row missing canonical keys {missing}"
        return
