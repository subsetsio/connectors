from subsets_utils import load_raw_parquet


def test_raw_assets_have_rows(spec_ids):
    for spec_id in spec_ids:
        table = load_raw_parquet(spec_id)
        assert table.num_rows > 1_000_000, f"{spec_id}: unexpectedly small raw table"


def test_emissions_release_shape(spec_ids):
    assert spec_ids == ["primap-hist-emissions"]
    table = load_raw_parquet("primap-hist-emissions")
    assert table.column_names == [
        "source",
        "scenario",
        "provenance",
        "area",
        "entity",
        "unit",
        "category",
        "year",
        "value",
        "release_version",
        "release_doi",
    ]
    years = table["year"].combine_chunks()
    assert years[0].as_py() >= 1750
    assert years[-1].as_py() >= 2024
