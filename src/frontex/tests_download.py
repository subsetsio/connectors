"""Health-invariant tests for the Frontex IBC connector.

Catch silent degradation the run's own validation misses: a truncated download,
a collapsed dimension set, or a span that stopped advancing.
"""
from subsets_utils import load_raw_parquet

_ASSET = "frontex-detections-of-ibc"


def test_raw_nonempty():
    """The long table should hold tens of thousands of (dimension, month) cells.
    A near-empty payload means the xlsx layout changed or the download truncated."""
    table = load_raw_parquet(_ASSET)
    assert len(table) >= 20000, f"{_ASSET}: only {len(table)} rows; expected >=20000"


def test_dimensions_present():
    """Several migratory routes and both Sea/Land border types must survive.
    A single route/type means the wide->long reshape collapsed."""
    table = load_raw_parquet(_ASSET)
    routes = set(table.column("route").to_pylist())
    btypes = set(table.column("border_type").to_pylist())
    assert len(routes) >= 5, f"{_ASSET}: only {len(routes)} distinct routes: {routes}"
    assert "Sea" in btypes and "Land" in btypes, f"{_ASSET}: border types missing: {btypes}"


def test_time_span_reaches_recent():
    """History starts in 2009; the latest month must be reasonably recent, else
    the monthly file stopped updating or we grabbed a stale link."""
    table = load_raw_parquet(_ASSET)
    months = table.column("month").to_pylist()
    assert min(months).year <= 2009, f"{_ASSET}: earliest month {min(months)} not <= 2009"
    assert max(months).year >= 2024, f"{_ASSET}: latest month {max(months)} not >= 2024"


def test_detections_nonnegative():
    """Detections are event counts; negatives signal a parse/sign error."""
    table = load_raw_parquet(_ASSET)
    import pyarrow.compute as pc
    assert pc.min(table.column("detections")).as_py() >= 0, f"{_ASSET}: negative detections found"
