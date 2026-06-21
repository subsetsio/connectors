"""Health-invariant tests for the Destatis download stage.

Run post-DAG, in-connector, against the data the download nodes wrote through
`subsets_utils`. They catch silent degradation that mere file existence misses:
empty payloads (auth/format break), non-numeric value columns, malformed dims.
"""

import json

from subsets_utils import load_raw_parquet


def test_assets_nonempty(spec_ids):
    """At least the large majority of statistics must have produced cells.

    A statistic legitimately may be tiny, but a wholesale empty corpus means the
    anonymous endpoint changed shape or started rejecting us. Sample a spread of
    specs and require most to hold rows."""
    sample = spec_ids[::17] or spec_ids
    empties = []
    for sid in sample:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            empties.append(sid)
    assert len(empties) <= len(sample) // 5, (
        f"{len(empties)}/{len(sample)} sampled statistics empty: {empties[:10]}"
    )


def test_row_shape(spec_ids):
    """Cells carry the expected columns, numeric values, and well-formed dims."""
    expected = {
        "statistic_code", "table_code", "table_name", "time",
        "measure_code", "dims", "value", "status",
    }
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if table.num_rows == 0:
            continue
        assert expected.issubset(set(table.column_names)), (
            f"{sid}: columns {table.column_names} missing {expected}"
        )
        head = table.slice(0, 200).to_pylist()
        for r in head:
            v = r["value"]
            assert v is None or isinstance(v, float), f"{sid}: non-float value {v!r}"
            parsed = json.loads(r["dims"])
            assert isinstance(parsed, dict), f"{sid}: dims not an object: {r['dims']!r}"
        values = table.column("value").to_pylist()
        assert any(v is not None for v in values), f"{sid}: every cell value is null"
        return  # one populated statistic is enough to validate shape
