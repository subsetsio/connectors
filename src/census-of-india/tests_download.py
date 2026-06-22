"""Health invariants for the Census of India raw assets.

Run post-DAG, in-connector, through the same subsets_utils loaders the fetch
nodes used. These catch silent degradation that mere file-existence misses:
empty payloads, a workbook layout the parser stopped recognizing, or values
that got coerced away.
"""

import json

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every entity must melt to at least some long rows. Zero rows means the
    download failed or the workbook layout drifted past the parser."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_long_shape_and_numeric_values(spec_ids):
    """Each row is a tidy (measure, value) cell with a numeric value and the
    fixed envelope columns present."""
    required = {"region", "dimensions", "measure", "value", "census_year",
                "table_code", "source_file"}
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[:2000]
        for r in sample:
            missing = required - r.keys()
            assert not missing, f"{sid}: row missing columns {missing}"
            assert r["value"] is not None, f"{sid}: null value leaked into raw"
            assert isinstance(r["value"], (int, float)), \
                f"{sid}: non-numeric value {r['value']!r}"
            assert r["measure"], f"{sid}: empty measure"
            # dimensions is a JSON object string
            assert isinstance(json.loads(r["dimensions"]), dict), \
                f"{sid}: dimensions is not a JSON object"


def test_measure_variety(spec_ids):
    """A real A-series table publishes several distinct measures; a single
    measure usually means the header block was misparsed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        measures = {r["measure"] for r in rows}
        assert len(measures) >= 3, \
            f"{sid}: only {len(measures)} distinct measure(s): {measures}"
