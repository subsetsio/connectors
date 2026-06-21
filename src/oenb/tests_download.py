"""Health invariants for the OeNB raw downloads."""

from subsets_utils import load_raw_parquet


def test_all_datasets_have_observations(spec_ids):
    """Every dataset must yield at least one observation. An empty asset means
    the position listing or the per-frequency /data probing silently broke
    (e.g. the dataset uses a frequency code we don't request)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 observations"


def test_rows_well_formed(spec_ids):
    """Spot-check that observations carry the keys the transform reads and that
    values are numeric — guards against an upstream format change."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        head = table.slice(0, min(200, table.num_rows)).to_pylist()
        for r in head:
            assert r.get("pos"), f"{sid}: row missing pos"
            assert r.get("period"), f"{sid}: row missing period"
            assert r.get("freq"), f"{sid}: row missing freq"
            assert isinstance(r.get("value"), float), (
                f"{sid}: value not numeric: {r.get('value')!r}"
            )
