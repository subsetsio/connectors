"""Health invariants for the Banco Central de Nicaragua connector.

These run post-DAG, in-connector, and catch silent degradation that file
existence alone misses: empty/truncated downloads, a parser that stopped
extracting rows, or values that all came back null.
"""
from subsets_utils import load_raw_parquet, load_state


def _ran_assets(spec_ids):
    """Spec ids that actually wrote raw (a permanent 4xx writes a TTL skip
    marker and no raw — exclude those so a transient source outage on one
    table doesn't mask the health of the rest)."""
    out = []
    for sid in spec_ids:
        skipped = load_state(sid).get("skipped", {})
        if skipped:
            continue
        out.append(sid)
    return out


def test_all_raw_assets_nonempty(spec_ids):
    """Every non-skipped spec's raw parquet should hold observation rows.
    Zero rows means the .xls layout changed or the parser silently broke."""
    empty = []
    for sid in _ran_assets(spec_ids):
        if len(load_raw_parquet(sid)) == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets have 0 rows: {empty[:10]}"


def test_values_present(spec_ids):
    """Each table must carry at least one non-null numeric value — an all-null
    column means cell parsing (thousands separators / missing tokens) drifted."""
    bad = []
    for sid in _ran_assets(spec_ids):
        t = load_raw_parquet(sid)
        if t.num_rows and t.column("value").null_count == t.num_rows:
            bad.append(sid)
    assert not bad, f"{len(bad)} assets have only null values: {bad[:10]}"


def test_years_plausible(spec_ids):
    """Years parsed from the first column must fall in a sane range; junk in
    that column (a stray note row read as data) would land outside it."""
    bad = []
    for sid in _ran_assets(spec_ids):
        t = load_raw_parquet(sid)
        if not t.num_rows:
            continue
        years = t.column("year").to_pylist()
        if min(years) < 1900 or max(years) > 2100:
            bad.append((sid, min(years), max(years)))
    assert not bad, f"implausible years: {bad[:10]}"
