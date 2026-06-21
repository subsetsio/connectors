"""Health invariants for Fannie Mae raw assets (run post-DAG, in-connector)."""

from subsets_utils import load_raw_ndjson

# Per-asset floor on parsed long-format row counts. Tuned to what each workbook
# actually yields (well below observed, above a degraded/empty parse).
_MIN_ROWS = {
    "fannie-mae-fannie-mae-hpi": 200,                     # ~200 quarters x 2 series
    "fannie-mae-nhs-monthly-indicator-data": 3000,        # ~186 months x ~40 indicators
    "fannie-mae-hpes-survey-history-panel": 300,          # pivot melt
    "fannie-mae-hpes-panelist-response-summary": 200,     # panelists x years x 2 metrics
    "fannie-mae-pali-rali-weekly": 5000,                  # ~1180 weeks x ~15 metrics
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce rows; empty means the workbook layout
    or download-link pattern changed and parsing silently fell through."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        floor = _MIN_ROWS.get(sid, 1)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows, expected >= {floor}"


def test_values_are_numeric(spec_ids):
    """The melted 'value' column must be numeric on every row — a wrong cell
    offset would smuggle header/label text into value."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        for row in rows[:500]:
            v = row.get("value")
            assert isinstance(v, (int, float)) and not isinstance(v, bool), (
                f"{sid}: non-numeric value {v!r} in {row}"
            )


def test_time_keys_present(spec_ids):
    """Each dataset carries its expected time/key dimension on every row."""
    key_by = {
        "fannie-mae-fannie-mae-hpi": "date",
        "fannie-mae-nhs-monthly-indicator-data": "date",
        "fannie-mae-hpes-survey-history-panel": "target_year",
        "fannie-mae-hpes-panelist-response-summary": "panelist",
        "fannie-mae-pali-rali-weekly": "week_ending",
    }
    for sid in spec_ids:
        key = key_by.get(sid)
        if not key:
            continue
        rows = load_raw_ndjson(sid)
        missing = [r for r in rows[:500] if r.get(key) in (None, "")]
        assert not missing, f"{sid}: {len(missing)} rows missing '{key}'"
