"""Health-invariant tests for the Eurostat connector (run post-DAG, in-connector).

Eurostat is a large catalog (~5.4k datasets); some entities 404 because they were
discontinued between collect and the run, so we sample and tolerate per-entity
absences rather than requiring every asset. What we DO assert: the datasets that
loaded carry the uniform long-format schema (time_period + value) and real
numeric observations — the signatures that catch a silent SDMX-CSV format change
or a broken parse.
"""
from subsets_utils import load_raw_ndjson


def test_sampled_assets_have_observations(spec_ids):
    # Spread the sample across the id space rather than the first N (which are
    # all 'aact_*'), so a format break in any neighbourhood is visible.
    step = max(1, len(spec_ids) // 50)
    sample = spec_ids[::step][:50]
    loaded = 0
    for sid in sample:
        try:
            rows = load_raw_ndjson(sid)
        except Exception:
            continue  # discontinued / 404-skipped dataset — fine in isolation
        if not rows:
            continue
        loaded += 1
        first = rows[0]
        assert "time_period" in first and "value" in first, (
            f"{sid}: row missing core keys; got {list(first)[:8]}"
        )
        assert any(r.get("value") is not None for r in rows[:500]), (
            f"{sid}: no numeric OBS_VALUE in first 500 rows — parse likely broke"
        )
        assert any(
            isinstance(r.get("value"), (int, float)) for r in rows[:500]
        ), f"{sid}: value column never numeric — type coercion broke"

    assert loaded >= 5, (
        f"only {loaded}/{len(sample)} sampled assets had rows; "
        "downloads may have broadly failed (format/auth/host change)"
    )
