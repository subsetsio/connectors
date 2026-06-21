"""Post-DAG health invariants for the NCSES connector.

Each NCSES data table is parsed to a tidy ndjson grid in the fetch fn; these
tests catch silent degradation (empty payloads, a format change that collapses
a table to one opaque column, or numeric coercion silently failing).
"""
import random

from subsets_utils import load_raw_ndjson


def test_sample_assets_wellformed(spec_ids):
    """A random sample of tables must hold rows with >=2 named columns. A
    truncated download or a header-parse regression shows up as 0 rows or a
    single catch-all column."""
    rng = random.Random(13)
    sample = rng.sample(spec_ids, min(25, len(spec_ids)))
    thin = []
    for sid in sample:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"
        cols = set()
        for r in rows[:50]:
            cols.update(r.keys())
        if len(cols) < 2:
            thin.append((sid, sorted(cols)))
    assert not thin, f"tables with <2 columns (parse likely broke): {thin[:5]}"


def test_numeric_typing_present(spec_ids):
    """Across the sample, at least one table must carry a numeric value —
    statistical tables are mostly numbers, so all-string output means the
    numeric coercion path is dead."""
    rng = random.Random(29)
    sample = rng.sample(spec_ids, min(25, len(spec_ids)))
    saw_numeric = False
    for sid in sample:
        rows = load_raw_ndjson(sid)
        for r in rows:
            if any(isinstance(v, (int, float)) for v in r.values()):
                saw_numeric = True
                break
        if saw_numeric:
            break
    assert saw_numeric, "no numeric values found across sampled tables"
