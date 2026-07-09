"""Health invariants over the whole CSO raw pull.

The per-spec YAML specs assert each matrix's own shape. These catch degradation
that only shows up across the corpus: a mass of empty payloads, a collapsing
schema, or PxStat quietly 404ing away a large slice of the accepted catalog.
"""

from subsets_utils import load_raw_parquet, load_state, raw_asset_exists

EXPECTED_COLUMNS = {
    "matrix",
    "statistic_code",
    "statistic_label",
    "time_code",
    "time_label",
    "time_dimension",
    "period_start",
    "period_end",
    "unit",
    "value",
}

# PxStat either serves an accepted matrix or it doesn't; a handful of retirements
# between collect and download is normal, a wave of them is a broken fetch.
MAX_SKIPPED_FRACTION = 0.02


def _skipped(spec_id: str) -> bool:
    return bool((load_state(spec_id) or {}).get("skipped"))


def test_every_spec_produced_raw_or_a_skip_marker(spec_ids):
    """A spec that wrote neither raw nor a 404 marker failed silently."""
    missing = [
        sid for sid in spec_ids if not raw_asset_exists(sid, "parquet") and not _skipped(sid)
    ]
    assert not missing, f"{len(missing)} specs produced no raw and no skip marker: {missing[:10]}"


def test_skipped_matrices_are_a_small_minority(spec_ids):
    """Mass 404s mean the endpoint or the id scheme moved, not that CSO retired 200 tables."""
    skipped = [sid for sid in spec_ids if _skipped(sid)]
    limit = max(1, int(len(spec_ids) * MAX_SKIPPED_FRACTION))
    assert len(skipped) <= limit, (
        f"{len(skipped)} of {len(spec_ids)} matrices 404'd (limit {limit}): {skipped[:10]}"
    )


def test_raw_assets_are_nonempty_and_well_formed(spec_ids):
    """Every fetched matrix holds rows, on the one schema the fetch fn normalizes to."""
    empty, malformed = [], []
    for sid in spec_ids:
        if not raw_asset_exists(sid, "parquet"):
            continue
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empty.append(sid)
        elif not EXPECTED_COLUMNS.issubset(set(table.column_names)):
            malformed.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"
    assert not malformed, f"{len(malformed)} assets miss normalized columns: {malformed[:10]}"


def test_values_are_not_universally_null(spec_ids):
    """Blank cells are suppression; an all-null corpus means VALUE stopped parsing."""
    fetched = [sid for sid in spec_ids if raw_asset_exists(sid, "parquet")]
    assert fetched, "no raw assets were fetched at all"
    with_values = 0
    for sid in fetched:
        table = load_raw_parquet(sid)
        if table.column("value").null_count < table.num_rows:
            with_values += 1
    assert with_values > len(fetched) // 2, (
        f"only {with_values} of {len(fetched)} matrices carry any non-null VALUE"
    )
