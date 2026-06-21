"""Health-invariant tests — run post-DAG, in-connector, after a real fetch.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, a WAF page served instead of data, or the registry parser
swallowing a format change.
"""
from subsets_utils import load_raw_parquet, load_raw_ndjson

_REGISTRY_IDS = {"faa-master", "faa-dereg", "faa-acftref", "faa-engine"}

# Coarse floors — well below true sizes, tight enough to trip a truncated pull.
_REGISTRY_MIN_ROWS = {
    "faa-master": 200_000,   # ~300k+ active registrations
    "faa-dereg": 100_000,    # large historical cancellation set
    "faa-acftref": 10_000,   # ~90k make/model refs
    "faa-engine": 1_000,     # ~4.7k engine refs
}
_ARCGIS_MIN_ROWS = {
    "faa-airports": 10_000,            # ~19.5k
    "faa-runways": 10_000,
    "faa-navaid-system": 500,
    "faa-navaid-component": 500,
    "faa-digital-obstacle-file": 100_000,  # ~640k
    "faa-frequency": 1_000,
    "faa-ils-system": 200,
    "faa-designated-point": 5_000,     # ~17k
}


def test_registry_assets_have_expected_volume(spec_ids):
    for sid in _REGISTRY_IDS & set(spec_ids):
        table = load_raw_parquet(sid)
        floor = _REGISTRY_MIN_ROWS[sid]
        assert table.num_rows >= floor, (
            f"{sid}: {table.num_rows} rows < expected floor {floor} — likely a "
            f"truncated download or a WAF/HTML page in place of the ZIP"
        )
        assert table.num_columns >= 5, f"{sid}: only {table.num_columns} columns parsed"


def test_arcgis_assets_have_expected_volume(spec_ids):
    for sid, floor in _ARCGIS_MIN_ROWS.items():
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, (
            f"{sid}: {len(rows)} features < expected floor {floor} — pagination "
            f"likely stopped after the first page or the layer returned an error"
        )
        assert "OBJECTID" in rows[0], f"{sid}: feature attributes missing OBJECTID"
