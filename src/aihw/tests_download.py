"""Post-DAG health invariants for the AIHW connector. These run in-connector
after the download nodes, loading raw assets through subsets_utils so they catch
silent degradation (empty payloads, truncated downloads, format switches) that
file-existence checks miss."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce a non-empty NDJSON raw asset. An empty
    payload usually means the CKAN resource URL changed or the MyHospitals
    endpoint silently switched format/returned an error envelope."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_rows_are_objects(spec_ids):
    """Each raw row must be a JSON object (dict). A list/str here means the CSV
    parse or the JSON flattening broke and we wrote the wrong shape."""
    for sid in spec_ids:
        first = load_raw_ndjson(sid)[0]
        assert isinstance(first, dict), f"{sid}: first raw row is {type(first).__name__}, not dict"
        assert first, f"{sid}: first raw row is an empty object"
