"""Post-DAG health invariants for the MAS download assets."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset must yield rows. An empty payload means list-rows changed
    shape, the cursor broke, or the dataset id went stale."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_raw_schema_shape(spec_ids):
    """Each raw record is either wide-unpivoted (data_series/period_raw/value_raw)
    or the native-long daily rate (date/exchange_rate_usd). Anything else means
    the upstream format drifted."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        keys = set(rows[0].keys())
        wide = {"data_series", "period_raw", "value_raw"} <= keys
        long = "date" in keys and "exchange_rate_usd" in keys
        assert wide or long, f"{sid}: unexpected raw schema {sorted(keys)}"
