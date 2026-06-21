"""Health invariants for the CFTC COT raw assets.

Reads via raw_reader (streaming, line-counted) rather than load_raw_ndjson so a
~570k-row family doesn't have to fully materialize in memory during the test.
"""
import json

from subsets_utils import raw_reader

# Minimum rows expected per family (both resources combined where applicable).
# Loose floors: legacy spans 1986+ across two resources; the 2006+ families are
# smaller. A run that trips these means pagination stopped after page 1 or a
# resource id changed.
MIN_ROWS = {
    "cftc-legacy": 300000,
    "cftc-disaggregated": 60000,
    "cftc-tff": 30000,
    "cftc-supplemental-cit": 5000,
}


def test_raw_assets_have_expected_rows(spec_ids):
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid, 1)
        n = 0
        first = None
        with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
            for line in f:
                if not line.strip():
                    continue
                if first is None:
                    first = json.loads(line)
                n += 1
        assert n >= floor, f"{sid}: {n} rows < expected floor {floor}"
        assert first is not None, f"{sid}: no records"
        assert "report_date_as_yyyy_mm_dd" in first, (
            f"{sid}: missing report_date_as_yyyy_mm_dd — schema drift"
        )
