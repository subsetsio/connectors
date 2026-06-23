from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "country", "region", "residence", "ethnicity", "socdem", "version", "ref_id",
    "year1", "year2", "type_lt", "sex", "age", "age_int",
    "mx", "qx", "lx", "dx", "Lx", "Tx", "ex", "ex_orig",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet must hold rows. An empty payload means
    the ZIP changed shape, the `res` member vanished, or the CSV stopped parsing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_life_tables_schema(spec_ids):
    """The HLD bulk CSV has a fixed 21-column layout; a column drop signals an
    upstream header change we must reconcile before publishing."""
    table = load_raw_parquet("hld-life-tables")
    assert EXPECTED_COLUMNS.issubset(set(table.column_names)), (
        f"missing columns: {EXPECTED_COLUMNS - set(table.column_names)}"
    )
