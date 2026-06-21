"""Post-DAG health invariants — catch silent degradation (empty payloads,
truncated snapshots, a group_by that quietly stopped returning groups)."""

from subsets_utils import load_raw_ndjson

_REFERENCE = {
    "openalex-funders": 20_000,
    "openalex-publishers": 5_000,
    "openalex-sources": 100_000,
    "openalex-institutions": 80_000,
    "openalex-topics": 4_000,
    "openalex-fields": 26,
    "openalex-sdgs": 17,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec wrote rows; an empty asset means the endpoint or
    snapshot path silently broke."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_reference_floor_counts():
    """Snapshot entities returned at least their expected magnitude — guards
    against a manifest that lost partitions or a half-streamed download."""
    for sid, floor in _REFERENCE.items():
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < floor {floor}"


def test_reference_have_ids_and_names():
    """Flattening preserved the primary key and display name on every record."""
    for sid in _REFERENCE:
        rows = load_raw_ndjson(sid)
        missing_id = sum(1 for r in rows if not r.get("id"))
        missing_name = sum(1 for r in rows if not r.get("display_name"))
        assert missing_id == 0, f"{sid}: {missing_id} rows missing id"
        # a tiny number of entities legitimately lack a display name; allow <1%
        assert missing_name <= max(1, len(rows) // 100), \
            f"{sid}: {missing_name}/{len(rows)} rows missing display_name"


def test_works_by_year_is_a_series():
    rows = load_raw_ndjson("openalex-works-by-year")
    years = {r["publication_year"] for r in rows}
    assert len(years) >= 30, f"works-by-year: only {len(years)} distinct years"
    assert all(r["works_count"] and r["works_count"] > 0 for r in rows), \
        "works-by-year: non-positive counts present"
    # the modern record-volume years must be present and large
    recent = [r["works_count"] for r in rows if 2015 <= r["publication_year"] <= 2024]
    assert recent and max(recent) > 5_000_000, \
        "works-by-year: recent-year counts implausibly small"


def test_dimension_year_covers_all_dimensions():
    rows = load_raw_ndjson("openalex-works-by-dimension-year")
    dims = {r["dimension"] for r in rows}
    expected = {"type", "oa_status", "domain", "field", "sdg"}
    assert dims == expected, f"dimension coverage {dims} != {expected}"
    # each dimension must carry a multi-year series, not a single snapshot row
    for d in expected:
        years = {r["publication_year"] for r in rows if r["dimension"] == d}
        assert len(years) >= 20, f"dimension {d}: only {len(years)} years"
