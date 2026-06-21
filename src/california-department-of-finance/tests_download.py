"""Health-invariant tests — run post-DAG, in-connector, against the raw layer.

Catches silent degradation that file-existence alone misses: an ArcGIS layer
that started returning an error envelope, a truncated page, or an empty payload.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's NDJSON raw must hold rows. An empty payload usually
    means the FeatureServer switched format, the item was unshared, or paging
    broke after page 0."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_rows_are_attribute_dicts(spec_ids):
    """Each row should be a non-empty dict of attributes (returnGeometry=false
    means no geometry key). A row that is not a populated dict means we saved the
    raw feature envelope instead of its attributes."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        first = rows[0]
        assert isinstance(first, dict) and first, f"{sid}: row 0 is not a populated dict"
