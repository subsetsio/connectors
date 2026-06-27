"""Health-invariant tests run post-DAG, in-connector, through subsets_utils
loaders. They catch silent degradation (empty payloads, dropped products,
schema collapse) that file-existence checks miss."""
from subsets_utils import load_raw_parquet

# Required identity/value columns per download asset.
_REQUIRED_COLS = {
    "lincoln-institute-atlas-areas-and-densities": {"city", "metric", "period", "value"},
    "lincoln-institute-atlas-blocks-and-roads-1": {"city", "metric", "period", "value"},
    "lincoln-institute-fisc-values": {"city", "state", "year", "category", "value"},
    "lincoln-institute-glance-property-tax-features": {"state", "year", "metric", "value"},
    "lincoln-institute-glance-selected-property-tax-statistics": {"state", "year", "metric", "value"},
    "lincoln-institute-glance-sources-of-local-general-revenue": {"state", "year", "metric", "value"},
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows. An empty payload usually means the
    endpoint switched format, the WAF started blocking, or a product went away."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_required_columns_present(spec_ids):
    """Each asset keeps its expected columns — guards against a header/shape
    change silently collapsing the long format."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _REQUIRED_COLS.get(sid, set()) - cols
        assert not missing, f"{sid}: missing expected columns {missing}"


def test_fisc_covers_many_cities(spec_ids):
    """FiSC should span the full central-city panel (~200 cities). A sharp drop
    means per-city POSTs are failing silently."""
    sid = "lincoln-institute-fisc-values"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    n_cities = len(set(table.column("city").to_pylist()))
    assert n_cities >= 150, f"{sid}: only {n_cities} cities (expected ~212)"
