"""Health-invariant tests run post-DAG, in-connector, through subsets_utils
loaders. They catch silent degradation (empty payloads, pagination capped after
page 1, format drift) that mere file existence misses."""
from subsets_utils import load_raw_ndjson

# Floors set well below observed volume so normal fluctuation passes but a
# degraded run (e.g. year crawl broke after page 1) trips the assertion.
MIN_ROWS = {
    "box-office-mojo-yearly-summary": 40,        # ~50 years (1977-2026)
    "box-office-mojo-domestic-yearly": 5000,     # ~50 yrs x ~150-200 releases
    "box-office-mojo-worldwide-yearly": 3000,    # ~50 yrs x worldwide releases
    "box-office-mojo-weekend-summary": 1500,     # ~45 tracked yrs x ~50 weekends
    "box-office-mojo-domestic-weekend": 40000,   # ~2300 weekends x ~30 rows
    "box-office-mojo-domestic-daily": 12000,     # ~45 tracked yrs x ~365 days
    "box-office-mojo-top-lifetime-grosses": 400, # multi-page chart
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows; an empty payload means the page
    format changed or parsing silently returned nothing."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson is empty"


def test_raw_assets_meet_volume_floor(spec_ids):
    """Per-asset row floors detect truncated crawls (year/weekend enumeration
    broke after the first page) rather than just total emptiness."""
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_ndjson(sid))
        assert n >= floor, f"{sid}: {n} rows < floor {floor} — crawl likely truncated"


def test_gross_strings_present(spec_ids):
    """A '$'-formatted gross column should appear in each asset's rows; its
    absence means the column map missed a header rename after a format change."""
    gross_cols = {
        "box-office-mojo-yearly-summary": "total_gross",
        "box-office-mojo-domestic-yearly": "gross",
        "box-office-mojo-worldwide-yearly": "worldwide",
        "box-office-mojo-weekend-summary": "overall_gross",
        "box-office-mojo-domestic-weekend": "gross",
        "box-office-mojo-domestic-daily": "top10_gross",
        "box-office-mojo-top-lifetime-grosses": "lifetime_gross",
    }
    for sid in spec_ids:
        col = gross_cols.get(sid)
        if col is None:
            continue
        rows = load_raw_ndjson(sid)
        sample = rows[: min(200, len(rows))]
        has_dollar = any("$" in (r.get(col) or "") for r in sample)
        assert has_dollar, f"{sid}: no '$' value found in column {col!r}"
