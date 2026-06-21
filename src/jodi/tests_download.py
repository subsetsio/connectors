"""Health invariants for the JODI-Oil raw download.

Catch silent degradation that file-existence alone misses: a truncated/empty
download, a dropped tier (only one of the two zips loaded), or a format change
that strips the expected long-format columns.
"""

import pyarrow.compute as pc

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "REF_AREA",
    "TIME_PERIOD",
    "ENERGY_PRODUCT",
    "FLOW_BREAKDOWN",
    "UNIT_MEASURE",
    "OBS_VALUE",
    "ASSESSMENT_CODE",
}

# Crude/upstream codes live only in the primary zip; refined-product codes only
# in the secondary zip. Requiring one of each guards against a dropped tier.
PRIMARY_PRODUCTS = {"CRUDEOIL", "TOTCRUDE", "NGL", "OTHERCRUDE"}
SECONDARY_PRODUCTS = {"GASOLINE", "JETKERO", "KEROSENE", "LPG", "NAPHTHA", "RESFUEL"}


def test_columns_present(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        missing = EXPECTED_COLUMNS - set(table.column_names)
        assert not missing, f"{sid}: missing columns {missing}"


def test_row_count_reasonable(spec_ids):
    """Both tiers together are ~18M rows; <5M means a tier was dropped or the
    download truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows >= 5_000_000, (
            f"{sid}: only {table.num_rows:,} rows; expected >=5,000,000"
        )


def test_both_tiers_loaded(spec_ids):
    """Confirm both the primary (crude) and secondary (refined) zips landed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        products = set(pc.unique(table.column("ENERGY_PRODUCT")).to_pylist())
        assert products & PRIMARY_PRODUCTS, (
            f"{sid}: no primary/crude products found ({PRIMARY_PRODUCTS})"
        )
        assert products & SECONDARY_PRODUCTS, (
            f"{sid}: no secondary/refined products found ({SECONDARY_PRODUCTS})"
        )
