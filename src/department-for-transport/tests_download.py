"""Health invariants for the DfT road-traffic raw assets.

Each download node streams a gzipped CSV (`<id>.csv.gz`). We read just the
header plus the first data row through the streaming raw reader — enough to
catch an empty payload, a truncated download, or a format switch (e.g. the
endpoint started returning HTML/JSON) without pulling the ~1GB raw_counts file
into memory.
"""

from subsets_utils import raw_reader


def test_all_raw_assets_have_header_and_rows(spec_ids):
    for sid in spec_ids:
        with raw_reader(sid, "csv.gz", mode="rt", compression="gzip") as f:
            header = f.readline()
            first_row = f.readline()
        assert header.strip(), f"{sid}: raw csv has no header line"
        assert "," in header, f"{sid}: header is not comma-delimited CSV: {header[:120]!r}"
        assert first_row.strip(), f"{sid}: raw csv has a header but no data rows"


def test_traffic_assets_have_expected_columns(spec_ids):
    """Spot-check that the count/aggregate columns we cast in the transforms are
    actually present in the raw header — a renamed/removed column upstream would
    otherwise only surface as a transform failure."""
    required = {
        "department-for-transport-dft-traffic-counts-aadf": ["count_point_id", "year", "all_motor_vehicles"],
        "department-for-transport-dft-traffic-counts-aadf-by-direction": ["count_point_id", "year", "direction_of_travel"],
        "department-for-transport-dft-traffic-counts-raw-counts": ["count_point_id", "count_date", "hour"],
        "department-for-transport-local-authority-traffic": ["local_authority_id", "year", "all_motor_vehicles"],
        "department-for-transport-region-traffic-by-road-type": ["region_id", "year", "road_category_id"],
        "department-for-transport-region-traffic-by-vehicle-type": ["region_id", "year", "all_motor_vehicles"],
    }
    for sid in spec_ids:
        cols = required.get(sid)
        if not cols:
            continue
        with raw_reader(sid, "csv.gz", mode="rt", compression="gzip") as f:
            header = f.readline().lower()
        missing = [c for c in cols if c.lower() not in header]
        assert not missing, f"{sid}: raw header missing expected columns {missing}"
