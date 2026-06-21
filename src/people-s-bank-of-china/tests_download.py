"""Health invariants for the PBOC raw assets — run post-DAG, in-connector."""
import re

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every table must yield rows. Empty means the portal layout changed or the
    title/category match silently failed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_record_shape(spec_ids):
    """Each record is a long-format observation with a parseable period and a
    numeric value."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(200, len(rows))]
        for r in sample:
            assert {"item", "period", "value"} <= set(r), f"{sid}: missing keys in {r}"
            assert r["item"], f"{sid}: empty item label"
            assert re.fullmatch(r"\d{4}-\d{2}", r["period"]), f"{sid}: bad period {r['period']!r}"
            assert isinstance(r["value"], (int, float)) and not isinstance(r["value"], bool), \
                f"{sid}: non-numeric value {r['value']!r}"


def test_multiple_periods(spec_ids):
    """A time series should span more than one month — a single period usually
    means only the latest file parsed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        periods = {r["period"] for r in rows}
        assert len(periods) >= 2, f"{sid}: only {len(periods)} distinct period(s)"
