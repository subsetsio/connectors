"""Post-DAG health invariants for the Freedom House raw assets.

These catch silent degradation that file-existence alone misses: an Excel layout
change that shifts the header row, a wide-block unpivot that collapses to a
handful of rows, or a workbook that starts returning an error page instead of
the spreadsheet.
"""
from subsets_utils import load_raw_ndjson

# Conservative floors — well below observed counts, tight enough that a broken
# parse (header moved, unpivot collapsed, wrong sheet) trips them.
_MIN_ROWS = {
    "freedom-house-fiw-all-data": 2000,
    "freedom-house-fiw-ratings-statuses": 7000,
    "freedom-house-nations-in-transit": 400,
    "freedom-house-freedom-on-the-net": 50,
    "freedom-house-freedom-of-the-press": 3000,
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_above_floor(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < floor {floor} (parse likely degraded)"


def test_years_parse_and_are_plausible(spec_ids):
    """Every row carries an int year in a sane range — guards against the year
    column landing in the wrong place after a layout change."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        bad = [r for r in rows if not isinstance(r.get("year"), int) or not (1970 <= r["year"] <= 2035)]
        assert not bad, f"{sid}: {len(bad)} rows with missing/implausible year (e.g. {bad[0] if bad else None})"


def test_score_columns_have_values(spec_ids):
    """The headline score on each panel is populated for a healthy share of rows
    — an all-null score column means values landed in the wrong column."""
    checks = {
        "freedom-house-fiw-all-data": "total",
        "freedom-house-nations-in-transit": "democracy_score",
        "freedom-house-freedom-on-the-net": "total",
        "freedom-house-fiw-ratings-statuses": "pr",
        "freedom-house-freedom-of-the-press": "total_score",
    }
    for sid, col in checks.items():
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        nonnull = sum(1 for r in rows if r.get(col) is not None)
        assert nonnull >= 0.4 * len(rows), (
            f"{sid}: only {nonnull}/{len(rows)} rows have a value for '{col}'"
        )
