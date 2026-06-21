"""Health invariants for the Bank of Italy raw assets.

Each raw asset is the ndjson of one Bollettino table's PROSPETTODATI
observations. Most tables are long-format records of {CUBEID, DATA_OSS, VALORE,
+SDMX dimensions}; a few use a measure-named wide layout where the value lives
in the column named by the row's MEASURES field and the date is in
DATA_DECOR/DATA_PROV (no DATA_OSS/VALORE). The invariants below accept both
shapes — they catch empty payloads and total format drift (the PROSPETTODATI
JSON shape changing under us), not a specific column set. Sampled to stay fast
over ~400 assets.
"""

import random

from subsets_utils import load_raw_ndjson

# Any of these naming a date column is enough to anchor an observation in time.
_DATE_FIELDS = ("DATA_OSS", "DATA_DECOR", "DATA_PROV")


def _sample(spec_ids, n):
    ids = list(spec_ids)
    return ids if len(ids) <= n else random.sample(ids, n)


def _numeric(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


def test_sample_assets_have_observations(spec_ids):
    """Every sampled table must hold observation records anchored in time.
    Empty payloads or a missing date field mean the fetch chain silently broke
    or the JSON shape drifted."""
    for sid in _sample(spec_ids, 25):
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, "%s: raw ndjson has 0 observations" % sid
        first = rows[0]
        assert any(k in first for k in _DATE_FIELDS), (
            "%s: record carries no date field %s — keys=%s"
            % (sid, _DATE_FIELDS, sorted(first.keys()))
        )


def test_values_are_numeric(spec_ids):
    """Each sampled table must yield at least one numeric value across the first
    rows — either a numeric VALORE (long format) or a numeric measure-named
    column (wide format). None numeric means the payload returned only status
    codes / dates, i.e. a format break."""
    for sid in _sample(spec_ids, 15):
        rows = load_raw_ndjson(sid)
        numeric = 0
        for r in rows[:200]:
            if _numeric(r.get("VALORE")):
                numeric += 1
                continue
            measure = r.get("MEASURES")
            if measure is not None and _numeric(r.get(measure)):
                numeric += 1
        assert numeric > 0, "%s: no numeric value in first 200 rows" % sid
