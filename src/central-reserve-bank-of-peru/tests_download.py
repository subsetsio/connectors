"""Health-invariant tests for the BCRP connector raw assets.

These run post-DAG, in-connector, against the data through subsets_utils
loaders — catching silent degradation (empty payloads, truncated downloads,
format drift) that file existence alone would miss.
"""
from subsets_utils import load_raw_ndjson, list_raw_files


def test_series_catalog_nonempty():
    rows = load_raw_ndjson("central-reserve-bank-of-peru-series")
    assert len(rows) >= 10000, f"series catalog has {len(rows)} rows; expected ~17k"
    assert all(r.get("series_code") for r in rows[:50]), "series rows missing series_code"


def test_groups_taxonomy_nonempty():
    rows = load_raw_ndjson("central-reserve-bank-of-peru-groups")
    assert len(rows) >= 300, f"groups taxonomy has {len(rows)} rows; expected ~640"


def test_values_batches_present_and_nonempty():
    """The values firehose must have written at least one batch with rows that
    carry the reshaped (series_code, date, value) shape."""
    batches = list_raw_files("central-reserve-bank-of-peru-values-*.ndjson.zst")
    assert batches, "no values batch files were written"
    total = 0
    saw_value = False
    for rel in batches:
        asset = rel[: -len(".ndjson.zst")]
        rows = load_raw_ndjson(asset)
        total += len(rows)
        for r in rows:
            assert "series_code" in r and "date" in r and "value" in r, f"bad row shape in {asset}"
            if r.get("value") is not None:
                saw_value = True
    assert total >= 1_000_000, f"values has only {total} observations; expected millions"
    assert saw_value, "no non-null observation values across all batches"
