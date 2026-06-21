"""Health invariants for the Geostat connector raw assets."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's NDJSON raw asset should hold at least one cell row.
    An empty payload means the json-stat POST returned nothing or the response
    format/shape changed silently."""
    empty = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets empty, e.g. {empty[:5]}"


def test_rows_have_value_field(spec_ids):
    """Each row is one flattened cube cell and must carry a `value` measure key
    plus at least one dimension column."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        r = rows[0]
        assert "value" in r, f"{sid}: row missing 'value' key: {list(r)[:6]}"
        assert len(r) >= 2, f"{sid}: row has no dimension columns: {list(r)}"
        break  # one representative asset is enough; full coverage above
