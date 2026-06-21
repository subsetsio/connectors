"""Health-invariant tests for the national-health-mission-hmis raw layer.

The hmis-values download writes one parquet batch per source report
(`<spec_id>-<resource_id>.parquet`), so we discover batches via list_raw_files
rather than loading the spec id directly.
"""

from subsets_utils import list_raw_files, load_raw_parquet

_VALUE_COLS = ("total", "public", "private", "urban", "rural")


def _batch_assets(spec_id: str) -> list[str]:
    files = list_raw_files(f"{spec_id}-*.parquet")
    return [f.split("/")[-1][: -len(".parquet")] for f in files]


def test_batches_exist_and_nonempty(spec_ids):
    """Every download spec must have produced at least one non-empty batch.
    No batches / empty batches mean the catalog filter or resource feed broke."""
    for sid in spec_ids:
        assets = _batch_assets(sid)
        assert assets, f"{sid}: no raw parquet batches found"
        total = sum(load_raw_parquet(a).num_rows for a in assets[:5])
        assert total > 0, f"{sid}: first batches all have 0 rows"


def test_long_schema_and_values(spec_ids):
    """A sampled batch must carry the normalised long schema and at least one
    populated breakdown value — guards a silent collapse to all-null measures."""
    for sid in spec_ids:
        assets = _batch_assets(sid)
        if not assets:
            continue
        t = load_raw_parquet(assets[0])
        cols = set(t.column_names)
        for required in ("state", "month", "parameter", "fy_start_year", *_VALUE_COLS):
            assert required in cols, f"{sid}: batch missing column {required!r}"
        # at least one measure value present somewhere in the sample
        import pyarrow.compute as pc
        nonnull = sum(t.column(c).null_count < t.num_rows for c in _VALUE_COLS)
        assert nonnull > 0, f"{sid}: every measure column is entirely null in {assets[0]}"
