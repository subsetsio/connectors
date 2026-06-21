"""Health-invariant tests run post-DAG inside the connector.

Each download node writes a faithful (string-valued) ndjson raw asset. These
tests catch silent degradation that file existence alone misses: an HTML error
page parsed into zero rows, a column rename upstream, a truncated pull.
"""

from subsets_utils import load_raw_ndjson

# Columns each raw asset must carry (the positional parse contract).
EXPECTED_KEYS = {
    "american-staffing-association-staffing-index": {
        "week_ending", "staffing_index", "wow_change", "four_week_average",
    },
    "american-staffing-association-bls-monthly-employment": {
        "series_id", "year", "period", "value",
    },
    "american-staffing-association-quarterly-employment-sales": {
        "year", "quarter", "sales", "payroll", "awe",
    },
    "american-staffing-association-gdp-quarterly-projections": {
        "year", "quarter", "first_estimate", "revised_final",
    },
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty payloads usually mean
    the gviz endpoint returned an HTML error page or auth/format changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_expected_columns_present(spec_ids):
    """The positional CSV parse must yield the agreed column keys; a column
    shift upstream would silently misalign values otherwise."""
    for sid in spec_ids:
        expected = EXPECTED_KEYS.get(sid)
        if not expected:
            continue
        rows = load_raw_ndjson(sid)
        keys = set(rows[0].keys())
        missing = expected - keys
        assert not missing, f"{sid}: raw rows missing expected keys {missing}"
