"""Health-invariant tests for federal-statistical-office raw assets.

These run post-DAG inside the connector and read raw via subsets_utils loaders,
so they behave identically locally and in the cloud. They catch silent
degradation that file-existence alone misses: empty payloads, lost value column,
missing provenance."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every cube's raw NDJSON must hold rows. An empty payload means the PxWeb
    selection returned nothing (format change, all-null cube, or a silent 403)."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} cubes have empty raw: {empty[:10]}"


def test_value_and_provenance_present(spec_ids):
    """Spot-check a sample: each row must carry a numeric `value` and a
    `cube_id`. A missing value column means the json-stat2 reshape broke."""
    import itertools
    for sid in itertools.islice(spec_ids, 25):
        rows = load_raw_ndjson(sid)
        head = rows[0]
        assert "value" in head and isinstance(head["value"], (int, float)), f"{sid}: bad value cell {head.get('value')!r}"
        assert head.get("cube_id"), f"{sid}: missing cube_id provenance"
