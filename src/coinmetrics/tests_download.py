"""Health-invariant tests for the coinmetrics connector.

Raw is written as row-bounded parquet batches with ids like
`coinmetrics-asset-metrics-00000`, so we discover them via list_raw_files and
read each batch back with the same loader the download node used.
"""

from subsets_utils import list_raw_files, load_raw_parquet

FAMILIES = ["coinmetrics-asset-metrics", "coinmetrics-institution-metrics"]


def _batch_ids(family: str) -> list[str]:
    """Asset ids of every parquet batch belonging to a family."""
    ids = set()
    for path in list_raw_files(f"{family}-*.parquet"):
        name = path.split("/")[-1][: -len(".parquet")]
        if name.startswith(family + "-") and name[len(family) + 1:].isdigit():
            ids.add(name)
    return sorted(ids)


def test_each_family_has_batches():
    """Both families must produce at least one parquet batch; none means the
    catalog enumeration or timeseries fetch broke silently."""
    for fam in FAMILIES:
        batches = _batch_ids(fam)
        assert batches, f"{fam}: no raw parquet batches written"


def test_batches_nonempty_and_long_shape():
    """Every batch holds rows in the uniform long schema."""
    cols = {"entity", "metric", "time", "value", "frequency"}
    for fam in FAMILIES:
        total = 0
        for sid in _batch_ids(fam):
            t = load_raw_parquet(sid)
            assert len(t) > 0, f"{sid}: empty parquet batch"
            assert cols.issubset(set(t.column_names)), (
                f"{sid}: missing long columns, got {t.column_names}"
            )
            total += len(t)
        assert total > 0, f"{fam}: zero rows across all batches"


def test_asset_metrics_breadth():
    """asset-metrics should span many assets and metrics — a collapse to a
    single asset/metric means catalog pagination capped at page 1."""
    fam = "coinmetrics-asset-metrics"
    entities, metrics = set(), set()
    for sid in _batch_ids(fam):
        t = load_raw_parquet(sid)
        entities.update(t.column("entity").to_pylist())
        metrics.update(t.column("metric").to_pylist())
    assert len(entities) >= 500, f"only {len(entities)} assets seen; expected many hundreds"
    assert len(metrics) >= 10, f"only {len(metrics)} distinct metrics; expected >=10"


def test_values_mostly_numeric():
    """The raw value column is numeric-as-string; a wholesale parse failure
    would mean the response format changed."""
    sid = _batch_ids("coinmetrics-asset-metrics")[0]
    t = load_raw_parquet(sid)
    vals = t.column("value").to_pylist()[:2000]
    bad = 0
    for v in vals:
        try:
            float(v)
        except (TypeError, ValueError):
            bad += 1
    assert bad / max(len(vals), 1) < 0.05, f"{bad}/{len(vals)} values non-numeric"
