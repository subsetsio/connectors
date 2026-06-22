"""Health-invariant tests for the asian-development-bank connector.

Run post-DAG, in-connector, against the raw assets the download nodes wrote
(all-string parquet of the KIDB SDMX-CSV). Catch silent degradation that file
existence alone misses: empty payloads, an endpoint that switched format, an
all-null value column.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataflow returns observations; 0 rows means the CSV endpoint
    404'd into an error page or the dataflow id stopped resolving."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """The SDMX-CSV header is stable; a missing core column means the
    server changed the response format."""
    required = {"INDICATOR", "ECONOMY_CODE", "TIME_PERIOD", "OBS_VALUE", "FREQ"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = required - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_obs_value_not_entirely_empty(spec_ids):
    """At least some observations carry a numeric value. An all-empty
    OBS_VALUE column means the data payload silently dropped."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("OBS_VALUE").to_pylist()
        nonempty = sum(1 for v in vals if v not in (None, ""))
        assert nonempty > 0, f"{sid}: OBS_VALUE is entirely empty"
