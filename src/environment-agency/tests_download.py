"""Post-DAG health invariants for the Environment Agency hydrology raw assets.

Guards against silent degradation: a list endpoint quietly paginating to one
page, the readings bulk endpoint changing format / returning a banner, or the
station/measure catalogs collapsing. Floors are well below observed live counts
(9.5k stations, 32k measures) but tight enough that a truncated payload trips.
"""

from subsets_utils import list_raw_files, load_raw_parquet

_FLOORS = {
    "environment-agency-stations": 5000,
    "environment-agency-measures": 20000,
}


def test_raw_assets_present(spec_ids):
    for sid in spec_ids:
        assert list_raw_files(f"{sid}.*"), f"{sid}: no raw file written"


def test_catalog_floors(spec_ids):
    for sid, floor in _FLOORS.items():
        if sid not in spec_ids:
            continue
        n = load_raw_parquet(sid).num_rows
        assert n >= floor, f"{sid}: {n} rows < floor {floor}"


def test_readings_nonempty_and_typed(spec_ids):
    sid = "environment-agency-readings"
    if sid not in spec_ids:
        return
    t = load_raw_parquet(sid)
    assert t.num_rows >= 10000, f"{sid}: only {t.num_rows} readings"
    cols = set(t.column_names)
    assert {"measure_id", "date", "value"} <= cols, f"{sid}: missing core cols {cols}"
    # measure_id is the join key to the measures catalog — must be populated.
    assert t.column("measure_id").null_count == 0, f"{sid}: null measure_id present"
