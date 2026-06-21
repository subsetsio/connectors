"""Health-invariant tests for the CelesTrak SATCAT downloads.

Each download writes the full SATCAT as parquet. These catch silent
degradation — a truncated download, a format change that drops orbital
data, or the catalog shrinking below a plausible floor.
"""
from subsets_utils import load_raw_parquet


_EXPECTED_COLS = {
    "object_name", "object_id", "norad_cat_id", "object_type",
    "ops_status_code", "owner", "launch_date", "launch_site",
    "decay_date", "period", "inclination", "apogee", "perigee",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every SATCAT download must hold the full catalog (~69k rows). A small
    table means the download truncated or the endpoint changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 50000, f"{sid}: only {len(table)} rows; expected >=50000"
        cols = set(table.column_names)
        missing = _EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing expected columns {missing}"


def test_satcat_has_orbital_and_history(spec_ids):
    """The catalog must carry orbital params for most objects and span the
    full space age — both vanish if the source format silently changes."""
    table = load_raw_parquet(spec_ids[0])

    periods = [p for p in table.column("period").to_pylist() if p is not None and p > 0]
    assert len(periods) > 10000, f"expected orbital data for >10000 objects, got {len(periods)}"

    types = set(table.column("object_type").to_pylist())
    assert "PAY" in types, "expected PAY (payload) objects"
    assert "DEB" in types, "expected DEB (debris) objects"

    launch_years = {
        d[:4] for d in table.column("launch_date").to_pylist() if d
    }
    assert "1957" in launch_years, "expected 1957 (Sputnik-era) launches"
    assert any(y.startswith("202") for y in launch_years), "expected recent (2020s) launches"
