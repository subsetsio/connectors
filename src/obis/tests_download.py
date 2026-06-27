"""Health invariants for the OBIS raw assets — catch silent degradation
(empty payloads, pagination capped after page 1, format switch)."""

from subsets_utils import load_raw_ndjson, load_raw_parquet

_NDJSON = {"obis-datasets", "obis-checklist"}


def _count(sid):
    if sid in _NDJSON:
        return len(load_raw_ndjson(sid))
    return len(load_raw_parquet(sid))


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        assert _count(sid) > 0, f"{sid}: raw asset has 0 rows"


def test_catalog_sizes(spec_ids):
    """Datasets (~6760) and checklist (~197k) are paginated; a collapse to a
    single page would slip far below these floors."""
    if "obis-datasets" in spec_ids:
        n = _count("obis-datasets")
        assert n >= 5000, f"obis-datasets: {n} rows, expected >=5000"
    if "obis-checklist" in spec_ids:
        n = _count("obis-checklist")
        assert n >= 150000, f"obis-checklist: {n} rows, expected >=150000"
