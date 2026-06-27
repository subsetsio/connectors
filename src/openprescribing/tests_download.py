"""Post-DAG health invariants — catch silent degradation the DAG would miss."""

from subsets_utils import load_raw_ndjson


def test_raw_assets_nonempty(spec_ids):
    """Every raw asset that ran should hold rows. Empty payloads usually mean the
    endpoint changed format, or (for the live API nodes) a Cloudflare 403 page
    slipped through as data instead of raising."""
    failures = []
    for sid in spec_ids:
        try:
            rows = load_raw_ndjson(sid)
        except Exception as exc:  # missing/corrupt asset
            failures.append(f"{sid}: load failed ({type(exc).__name__}: {exc})")
            continue
        if not rows:
            failures.append(f"{sid}: 0 rows")
    assert not failures, "; ".join(failures)


def test_measures_catalog_populated(spec_ids):
    """The measures catalog is repo-sourced and should always carry the full set
    of curated measures with stable ids."""
    sid = "openprescribing-measures"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 50, f"only {len(rows)} measures; expected >=50"
    ids = [r.get("measure_id") for r in rows]
    assert all(ids), "some measures have a null measure_id"
    assert len(set(ids)) == len(ids), "duplicate measure_id in catalog"
