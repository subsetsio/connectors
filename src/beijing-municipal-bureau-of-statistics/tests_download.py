"""Health invariants for the Beijing macro-DB raw assets.

Run post-DAG, in-connector, through the same subsets_utils loader the download
node used (NDJSON). Catches silent degradation that file-existence alone misses:
empty payloads, the session-seeding regressing to ``[]`` data, or the cell
unflatten producing rows with no indicator/value.
"""
from subsets_utils import load_raw_ndjson


def test_some_raw_assets_nonempty(spec_ids):
    """Across the corpus, the great majority of reports must yield rows. A
    handful of genuinely-empty report tables is tolerable, but if almost
    everything is empty the session seeding / data call has regressed to []."""
    nonempty = 0
    checked = 0
    for sid in spec_ids:
        try:
            rows = load_raw_ndjson(sid)
        except FileNotFoundError:
            continue
        checked += 1
        if rows:
            nonempty += 1
    assert checked > 0, "no raw assets were produced"
    frac = nonempty / checked
    assert frac >= 0.5, (
        f"only {nonempty}/{checked} reports produced rows ({frac:.0%}); "
        "expected the majority to have data — session seeding may have failed"
    )


def test_rows_well_formed(spec_ids):
    """Every persisted row must carry its report_number, an indicator label, and
    a non-empty value — the three fields the transform depends on."""
    for sid in spec_ids:
        try:
            rows = load_raw_ndjson(sid)
        except FileNotFoundError:
            continue
        for row in rows[:200]:
            assert row.get("report_number"), f"{sid}: row missing report_number"
            assert row.get("indicator"), f"{sid}: row missing indicator"
            assert str(row.get("value", "")).strip() != "", f"{sid}: empty value persisted"
