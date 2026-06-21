"""Health invariants for the UN Statistics Division raw assets.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, or a format switch that drops the value/observation columns.
"""
from subsets_utils import load_raw_parquet, load_raw_file

SDG_ID = "un-statistics-division-sdg-data"


def test_sdg_observations_present(spec_ids):
    """The SDG database is the flagship — it should hold hundreds of thousands
    of observations with the expected columns."""
    if SDG_ID not in spec_ids:
        return
    t = load_raw_parquet(SDG_ID)
    assert t.num_rows > 100_000, f"{SDG_ID}: only {t.num_rows} rows (expected >100k)"
    for col in ("series", "value", "time_period", "geo_area_code"):
        assert col in t.column_names, f"{SDG_ID}: missing column {col}"
    nn = sum(1 for v in t.column("value").to_pylist() if v not in (None, ""))
    assert nn > 0, f"{SDG_ID}: no non-null values"


def test_sdmx_flows_nonempty(spec_ids):
    """Each SDMX dataflow csv must carry a header plus data rows and an
    OBS_VALUE column."""
    for sid in spec_ids:
        if sid == SDG_ID:
            continue
        text = load_raw_file(sid, extension="csv")
        lines = text.splitlines()
        assert len(lines) >= 2, f"{sid}: csv has {len(lines)} lines (expected header + rows)"
        assert "OBS_VALUE" in lines[0], f"{sid}: header missing OBS_VALUE: {lines[0][:120]}"
