"""Health-invariant tests for the SEER connector raw assets.

Run post-DAG, in-connector. They catch silent degradation that file existence
alone misses: empty payloads, a dimension grid that collapsed to a single combo,
or measure columns that lost their numeric type.

`spec_ids` carries every spec that ran — both the download nodes and their
`-transform` leaves. Only the download nodes write raw NDJSON, so we filter to
those before loading.
"""

from subsets_utils import load_raw_ndjson


def _download_ids(spec_ids):
    return [s for s in spec_ids if not s.endswith("-transform")]


def test_all_raw_assets_nonempty(spec_ids):
    """Every download's raw NDJSON should hold rows. Empty means the JSON backend
    changed shape or every (data_type, graph_type) site was filtered out."""
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_multiple_cancer_sites(spec_ids):
    """Each table spans many cancer sites (we loop every valid site and stamp the
    site onto every row). If fewer than 2 'site' values survive, the per-site loop,
    the validity gate, or the site-stamping broke."""
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        sites = {r.get("site") for r in rows if r.get("site") is not None}
        assert len(sites) >= 2, f"{sid}: only {len(sites)} distinct cancer site(s); expected many"


def test_single_schema(spec_ids):
    """Each download's rows must share one column set. Mixed column sets mean a
    foreign-schema fallback response leaked past the signature filter."""
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        colsets = {tuple(sorted(r.keys())) for r in rows[:20000]}
        assert len(colsets) == 1, f"{sid}: {len(colsets)} distinct column sets in raw rows"


def test_measures_numeric(spec_ids):
    """At least one numeric measure value is present per asset — guards against a
    decode/cast regression that would stringify every measure."""
    measure_fields = (
        "rate", "rate_lower_ci", "rate_upper_ci", "modeled_rate", "count",
        "percent", "risk", "median_age", "rate_se",
        "rel_rate", "modeled_rel_rate",
    )
    for sid in _download_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        ok = any(
            isinstance(r.get(f), (int, float)) and not isinstance(r.get(f), bool)
            for r in rows[:5000]
            for f in measure_fields
        )
        assert ok, f"{sid}: no numeric measure value found in first rows"
