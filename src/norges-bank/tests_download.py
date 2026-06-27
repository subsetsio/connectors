"""Health invariants for the Norges Bank raw assets (post-DAG, in-connector)."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow's raw NDJSON must hold observations. Empty payloads mean
    the 'all' query returned nothing — format/endpoint drift or a silent 4xx."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_core_columns_present(spec_ids):
    """Every SDMX observation row carries TIME_PERIOD and OBS_VALUE; their
    absence means the CSV component-id columns were not parsed correctly."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert "TIME_PERIOD" in sample, f"{sid}: no TIME_PERIOD column (keys={list(sample)})"
        assert "OBS_VALUE" in sample, f"{sid}: no OBS_VALUE column (keys={list(sample)})"
