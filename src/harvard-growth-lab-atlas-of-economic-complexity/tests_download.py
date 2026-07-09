"""Health invariants over the raw assets the download DAG just wrote.

These catch silent degradation that file existence alone misses: an empty or
truncated payload, a column that arrived all-null because the source stopped
populating it, a classification code parsed as an integer so its leading zeros
are gone.

An entity built from one source CSV is a plain `<spec_id>.parquet`; one built
from several is a set of `<spec_id>-<file_stem>.parquet` fragments. Both layouts
are enumerated through the same loaders the download node wrote them with. The
fragments are loaded one at a time and released -- the largest is a ~1 GB
country-product-year table, and holding them all at once would not fit.
"""

import pyarrow.types as pat

from subsets_utils import list_raw_files, load_raw_parquet

# Entities with no time dimension: dimension tables, the product-space network,
# and the classification conversion tables.
NON_TEMPORAL = {
    "location-country", "location-group", "top-edges-hs92", "umap-layout-hs92",
    "product-hs92", "product-hs12", "product-hs22", "product-sitc",
    "product-services-unilateral", "weighted-classification-conversion-tables",
}


def _part_ids(spec_id):
    """Every parquet object making up this spec's raw asset."""
    names = [p[: -len(".parquet")] for p in list_raw_files(f"{spec_id}*.parquet")]
    assert names, f"{spec_id}: no raw parquet written"
    return names


def _iter_parts(spec_id):
    for name in _part_ids(spec_id):
        yield load_raw_parquet(name)


def _first_schema(spec_id):
    return next(_iter_parts(spec_id)).schema


def test_all_raw_assets_nonempty(spec_ids):
    """A zero-row asset means the endpoint changed format, or the stream was cut
    before any batch landed."""
    for sid in spec_ids:
        rows = sum(t.num_rows for t in _iter_parts(sid))
        assert rows > 0, f"{sid}: raw parquet has 0 rows"


def test_fragments_share_one_schema(spec_ids):
    """Every fragment of an entity is written under that entity's union schema.
    A drifting fragment would make the transform's globbed view unreadable."""
    for sid in spec_ids:
        first = None
        for table in _iter_parts(sid):
            if first is None:
                first = table.schema
            else:
                assert table.schema.equals(first), (
                    f"{sid}: fragment schema drift\n  {first}\n  vs\n  {table.schema}"
                )


def test_temporal_assets_carry_year(slug, spec_ids):
    """Every trade table is a yearly series. A missing `year` means the wrong
    file was selected into the entity."""
    for sid in spec_ids:
        if sid[len(slug) + 1:] in NON_TEMPORAL:
            continue
        names = _first_schema(sid).names
        assert "year" in names, f"{sid}: no 'year' column ({names})"


def test_product_codes_are_strings(spec_ids):
    """HS '0101' is not the integer 101. A numeric code column means leading
    zeros were destroyed at parse time, and every downstream join against the
    classification tables would silently lose rows."""
    for sid in spec_ids:
        schema = _first_schema(sid)
        for name in schema.names:
            if name.endswith("_code") or "_code_" in name:
                field_type = schema.field(name).type
                assert pat.is_string(field_type), (
                    f"{sid}.{name}: expected string, got {field_type}"
                )


def test_no_all_null_columns(spec_ids):
    """A column null in every row of every fragment is one the source stopped
    populating, or one we mis-parsed. Depth-specific metrics (pci, export_rca)
    are legitimately null in *some* fragments, so this fires only when nothing
    anywhere carries a value."""
    for sid in spec_ids:
        rows = 0
        nulls = None
        for table in _iter_parts(sid):
            rows += table.num_rows
            counts = {n: table.column(n).null_count for n in table.schema.names}
            if nulls is None:
                nulls = counts
            else:
                for n, c in counts.items():
                    nulls[n] += c
        for name, null_count in nulls.items():
            assert null_count < rows, f"{sid}.{name}: all {rows} values are null"
