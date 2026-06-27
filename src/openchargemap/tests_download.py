"""Health-invariant tests for the Open Charge Map connector.

Run post-DAG inside the connector, reading raw through subsets_utils loaders so
they behave identically locally and in the cloud. These guard against silent
degradation that file-existence alone misses — a truncated tarball download,
an empty referencedata payload, or a format switch upstream.
"""

from subsets_utils import load_raw_parquet


def test_pois_nonempty_and_large(spec_ids):
    """The POI export is the whole global corpus (~266k locations across ~126
    countries). A tiny count almost always means the tarball download was
    truncated before EOF rather than a real shrink in the source."""
    if "openchargemap-pois" not in spec_ids:
        return
    t = load_raw_parquet("openchargemap-pois")
    assert len(t) >= 150_000, f"openchargemap-pois: only {len(t)} POIs — truncated tarball?"
    countries = set(t.column("country_code").to_pylist())
    assert len(countries) >= 100, f"openchargemap-pois: only {len(countries)} country codes"


def test_pois_have_coordinates(spec_ids):
    """Coordinates are mandatory in OCM; if the bulk of rows lack lat/lon the
    AddressInfo parsing path broke."""
    if "openchargemap-pois" not in spec_ids:
        return
    t = load_raw_parquet("openchargemap-pois")
    lat = t.column("latitude").to_pylist()
    have = sum(1 for v in lat if v is not None)
    assert have >= 0.95 * len(lat), f"openchargemap-pois: only {have}/{len(lat)} rows have latitude"


def test_operators_nonempty(spec_ids):
    """The operator directory had ~968 rows on probing; an empty/near-empty
    table means referencedata.json changed shape or returned an error body."""
    if "openchargemap-operators" not in spec_ids:
        return
    t = load_raw_parquet("openchargemap-operators")
    assert len(t) >= 700, f"openchargemap-operators: only {len(t)} operators"
