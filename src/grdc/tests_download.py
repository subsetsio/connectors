"""Health-invariant tests for the GRDC connector raw assets.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, the catalogue endpoint switching shape.
"""

from subsets_utils import load_raw_ndjson


def test_catalogue_nonempty_and_complete(spec_ids):
    """The station catalogue must hold the full network (~11,879 rows). An
    empty or sharply-truncated payload usually means the endpoint changed
    format or returned an error body that still parsed as JSON."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= 10000, f"{sid}: only {len(rows)} station records (expected ~11,879)"


def test_catalogue_core_fields_present(spec_ids):
    """Core identity/stat fields must be present on the records; if they vanish
    the upstream JSON schema changed and the transform would break."""
    required = {"grdc_no", "river", "station", "country", "lat", "long", "area", "lta_discharge"}
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        missing = required - set(sample.keys())
        assert not missing, f"{sid}: record missing core fields {sorted(missing)}"
