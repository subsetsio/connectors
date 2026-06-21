"""Health-invariant tests for the OECD connector (run post-DAG, in-connector).

OECD is a large SDMX catalog (~1.4k dataflows); some entities 404/500 because
they are external references with no data in OECD's mapping store, or were
withdrawn between collect and the run. We therefore sample across the id space
and tolerate per-entity absences rather than requiring every asset. What we DO
assert: the dataflows that loaded carry the uniform long-format schema
(time_period + value) and real numeric observations — the signatures that catch
a silent SDMX-CSV format change or a broken parse.
"""
from subsets_utils import load_raw_ndjson


def test_sampled_assets_have_observations(spec_ids):
    # Spread the sample across the id space rather than the first N (which all
    # share a leading agency), so a format break anywhere is visible.
    step = max(1, len(spec_ids) // 60)
    sample = spec_ids[::step][:60]
    loaded = 0
    for sid in sample:
        try:
            rows = load_raw_ndjson(sid)
        except Exception:
            continue  # discontinued / 404-skipped dataflow — fine in isolation
        if not rows:
            continue
        loaded += 1
        first = rows[0]
        assert "time_period" in first and "value" in first, (
            f"{sid}: row missing core keys; got {list(first)[:8]}"
        )
        assert any(r.get("value") is not None for r in rows[:1000]), (
            f"{sid}: no numeric OBS_VALUE in first 1000 rows — parse likely broke"
        )
        assert any(
            isinstance(r.get("value"), (int, float)) for r in rows[:1000]
        ), f"{sid}: value column never numeric — type coercion broke"

    assert loaded >= 5, (
        f"only {loaded}/{len(sample)} sampled assets had rows; "
        "downloads may have broadly failed (format/auth/host change)"
    )
