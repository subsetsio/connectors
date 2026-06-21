"""Health invariants for the ILO connector raw layer.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
node used. They catch silent degradation (empty payloads, format switches,
all-null values) that mere file existence would miss.
"""
import pyarrow.compute as pc

from subsets_utils import load_raw_parquet

# Columns every normalized indicator file must carry (the fixed RAW_SCHEMA core).
_REQUIRED_COLS = {
    "ref_area", "source", "indicator", "time_period", "obs_value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator file in the TOC has records; an empty raw parquet means
    the endpoint changed format or returned an error page silently."""
    empty = []
    for sid in spec_ids:
        if load_raw_parquet(sid).num_rows == 0:
            empty.append(sid)
    assert not empty, f"{len(empty)} raw assets are empty, e.g. {empty[:5]}"


def test_schema_stable(spec_ids):
    """The normalized parquet schema must hold across assets — if the fetch
    normalization broke, required columns would go missing."""
    bad = []
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        if not _REQUIRED_COLS <= cols:
            bad.append((sid, _REQUIRED_COLS - cols))
    assert not bad, f"{len(bad)} assets missing required columns, e.g. {bad[:5]}"


def test_obs_value_has_data(spec_ids):
    """At least some observations carry a numeric value. An all-null obs_value
    across an asset means parsing silently dropped the measure column."""
    allnull = []
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("obs_value")
        if pc.sum(pc.is_valid(col)).as_py() == 0:
            allnull.append(sid)
    # tolerate a tiny tail of genuinely metadata-only indicators, but the bulk
    # must carry values
    assert len(allnull) < max(5, len(spec_ids) * 0.02), (
        f"{len(allnull)} assets have all-null obs_value, e.g. {allnull[:5]}"
    )
