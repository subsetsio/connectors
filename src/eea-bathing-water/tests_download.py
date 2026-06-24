"""Health-invariant tests run post-DAG, in-connector, against the raw assets.
Catches silent degradation that file existence alone misses: empty payloads,
truncated pulls, or a column vanishing because the endpoint changed shape."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every WISE_BWD table is substantial (smallest is the country-aggregated
    view at a few thousand rows). A 0-row parquet means the SQL gateway returned
    an empty/error envelope or pagination broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_reporting_year_column_present(spec_ids):
    """Every WISE_BWD view is keyed to a reporting year — `season` on all the
    assessment/timeseries views, `cYear` on the spatial protected-area view.
    Absence means the projection silently changed shape."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols & {"season", "cYear"}, (
            f"{sid}: no reporting-year column (season/cYear); columns={sorted(cols)}"
        )
