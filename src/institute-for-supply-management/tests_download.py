"""Health invariants for the ISM raw downloads (long-format parquet per dataset)."""

from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {"date", "metric", "series_code", "series_name", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's raw parquet must hold observations. An empty payload
    means DBnomics changed the response shape or the dataset code went stale."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    """Long-format schema is the transform's contract; a missing column breaks
    the pivot."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_values_are_finite(spec_ids):
    """Diffusion indices and percentages sit in plausible ranges. Wildly
    out-of-band values flag a parse/scale error (e.g. ratios read as ints)."""
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value").to_pylist()
        assert col, f"{sid}: no values"
        assert all(v is not None for v in col), f"{sid}: null value slipped through"
        assert all(-50.0 <= v <= 200.0 for v in col), (
            f"{sid}: value out of plausible diffusion/percent range "
            f"(min={min(col)}, max={max(col)})"
        )


def test_headline_pmi_present(spec_ids):
    """The two headline PMIs must publish a 'pmi' metric — a sanity check on the
    metric-slug mapping and the right provider."""
    for sid in ("institute-for-supply-management-pmi", "institute-for-supply-management-nm-pmi"):
        if sid not in spec_ids:
            continue
        metrics = set(load_raw_parquet(sid).column("metric").to_pylist())
        assert "pmi" in metrics, f"{sid}: expected a 'pmi' metric, got {metrics}"
