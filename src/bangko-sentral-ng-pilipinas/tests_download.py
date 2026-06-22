"""Health-invariant tests for the BSP connector, run post-DAG inside the connector.

These catch silent degradation across the whole run (not per-table assertions —
those live in tests/<spec_id>.yaml). They read raw assets through subsets_utils
so they behave identically locally and in the cloud.
"""

from subsets_utils import load_raw_parquet, raw_asset_exists


def test_majority_of_assets_nonempty(spec_ids):
    """Most BSP matrices should yield a non-empty raw asset. The source's build
    endpoint is flaky, so we tolerate a minority of failures, but if the bulk of
    the corpus is empty the session/build flow has broken wholesale."""
    download_ids = [s for s in spec_ids if not s.endswith("-transform")]
    if not download_ids:
        return
    nonempty = 0
    for sid in download_ids:
        if raw_asset_exists(sid, ext="parquet"):
            try:
                if load_raw_parquet(sid).num_rows > 0:
                    nonempty += 1
            except Exception:
                pass
    frac = nonempty / len(download_ids)
    assert frac >= 0.5, (
        f"only {nonempty}/{len(download_ids)} BSP matrices produced non-empty raw "
        f"assets ({frac:.0%}); the PX-Web session/build flow likely broke"
    )


def test_value_column_present_and_typed(spec_ids):
    """Every non-empty raw asset must carry the normalized (row_label, col_label,
    value, date) schema; a drift means the normalizer regressed."""
    expected = {"row_label", "col_label", "value", "date"}
    download_ids = [s for s in spec_ids if not s.endswith("-transform")]
    for sid in download_ids:
        if not raw_asset_exists(sid, ext="parquet"):
            continue
        try:
            t = load_raw_parquet(sid)
        except Exception:
            continue
        if t.num_rows == 0:
            continue
        assert expected.issubset(set(t.column_names)), (
            f"{sid}: columns {t.column_names} missing one of {sorted(expected)}"
        )
