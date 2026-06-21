"""Post-download health invariants for the CBN connector."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every GetAll* endpoint returns a non-empty JSON array. An empty payload
    means the endpoint switched format (XML), moved, or Cloudflare served a
    challenge instead of data."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_rows_are_objects(spec_ids):
    """Each record must be a flat JSON object (dict) with at least one field —
    guards against the API returning a bare list of scalars or an error blob."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert isinstance(first, dict) and first, (
            f"{sid}: expected dict records, got {type(first).__name__}"
        )


def test_flagship_volume(spec_ids):
    """The high-traffic flagship series should carry a substantial history; a
    sudden collapse to a handful of rows signals a truncated/partial response."""
    expectations = {
        "central-bank-of-nigeria-getallexchangerates": 1000,
        "central-bank-of-nigeria-getallinterbankrates": 1000,
        "central-bank-of-nigeria-getallinflationrates": 100,
        "central-bank-of-nigeria-getallmoneyandcreditstats": 100,
    }
    for sid, floor in expectations.items():
        if sid in spec_ids:
            n = len(load_raw_ndjson(sid))
            assert n >= floor, f"{sid}: only {n} rows; expected >= {floor}"
