"""Health invariants for the DfT road-traffic raw assets.

Each download node writes a single Parquet file (`<id>.parquet`). We read only
the Parquet footer (row count + schema) so even the ~5M-row raw_counts asset is
checked without loading its data — enough to catch an empty payload, a truncated
download, or a format/column switch upstream.
"""

import pyarrow.parquet as pq

from subsets_utils import raw_reader

_REQUIRED_COLUMNS = {
    "department-for-transport-dft-traffic-counts-aadf": ["count_point_id", "year", "all_motor_vehicles"],
    "department-for-transport-dft-traffic-counts-aadf-by-direction": ["count_point_id", "year", "direction_of_travel"],
    "department-for-transport-dft-traffic-counts-raw-counts": ["count_point_id", "count_date", "hour"],
    "department-for-transport-local-authority-traffic": ["local_authority_id", "year", "all_motor_vehicles"],
    "department-for-transport-region-traffic-by-road-type": ["region_id", "year", "road_category_id"],
    "department-for-transport-region-traffic-by-vehicle-type": ["region_id", "year", "all_motor_vehicles"],
}


def _footer(sid):
    with raw_reader(sid, "parquet", mode="rb") as f:
        pf = pq.ParquetFile(f)
        return pf.metadata.num_rows, set(pf.schema_arrow.names)


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        n_rows, _ = _footer(sid)
        assert n_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_assets_have_expected_columns(spec_ids):
    """A renamed/removed source column would otherwise only surface as a
    downstream transform failure; catch it here against the raw schema."""
    for sid in spec_ids:
        want = _REQUIRED_COLUMNS.get(sid)
        if not want:
            continue
        _, names = _footer(sid)
        lowered = {n.lower() for n in names}
        missing = [c for c in want if c.lower() not in lowered]
        assert not missing, f"{sid}: raw parquet missing expected columns {missing}"
