"""Health-invariant tests for the Argo Program raw assets.

Run post-DAG, in-connector, through subsets_utils loaders so they behave the
same locally and in the cloud. They catch silent degradation (empty payloads,
format switches) that file-existence alone misses.
"""

from subsets_utils import list_raw_files, load_raw_parquet

# Single-file assets (re-pulled whole each run) vs time-windowed firehoses.
SINGLETONS = {"argo-program-argofloats-index", "argo-program-oacp-argo-global"}


def test_singleton_assets_nonempty(spec_ids):
    """The index and the climatology grid are re-pulled in full every run, so
    they must always materialize with rows. Empty means the endpoint changed
    format or the query silently broke."""
    for sid in spec_ids:
        if sid in SINGLETONS:
            table = load_raw_parquet(sid)
            assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_timeseries_batches_nonempty(spec_ids):
    """Firehose windows are only written when they contain rows, so every batch
    file that exists must be non-empty. A zero-row batch file means a window
    with data was truncated to nothing on our side. (We don't require batches to
    exist yet — a fresh backfill may still be walking sparse early years.)"""
    for sid in spec_ids:
        if sid in SINGLETONS:
            continue
        for rel in list_raw_files(f"{sid}-*.parquet"):
            asset = rel.split("/")[-1]
            if asset.endswith(".parquet"):
                asset = asset[: -len(".parquet")]
            table = load_raw_parquet(asset)
            assert len(table) > 0, f"{asset}: firehose batch file has 0 rows"


def test_index_has_netcdf_paths(spec_ids):
    """The profile index keys each row by a GDAC NetCDF profile path; if those
    stop ending in .nc the upstream index schema changed."""
    sid = "argo-program-argofloats-index"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    files = [f for f in table.column("file").to_pylist() if f]
    assert files, f"{sid}: no file paths present"
    nc = sum(1 for f in files[:5000] if f.endswith(".nc"))
    assert nc >= 0.95 * min(len(files), 5000), f"{sid}: <95% of file paths end in .nc"
