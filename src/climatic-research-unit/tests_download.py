"""Health-invariant tests for the Climatic Research Unit connector.

Run post-DAG inside the connector; they read raw assets through the same
subsets_utils loader the download nodes used to write them, so they behave
identically locally and in the cloud.
"""
from subsets_utils import load_raw_parquet

TEMP_IDS = [
    "climatic-research-unit-hadcrut5-analysis",
    "climatic-research-unit-hadcrut5-noninfilled",
    "climatic-research-unit-crutem5",
    "climatic-research-unit-crutem5alt",
    "climatic-research-unit-hadsst4",
]
COUNTRY_ID = "climatic-research-unit-cru-cy-country"


def test_temperature_assets_nonempty_three_regions(spec_ids):
    """Each temperature product must hold rows for all three regions; a missing
    region usually means a region file 404'd and was silently skipped."""
    for sid in TEMP_IDS:
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"
        regions = set(table.column("region").to_pylist())
        assert regions == {"nh", "sh", "gl"}, f"{sid}: regions={regions}"


def test_country_asset_complete(spec_ids):
    """CRU CY must carry all 10 variables and a broad country set; truncation
    of either the variable loop or a directory listing trips this."""
    if COUNTRY_ID not in spec_ids:
        return
    table = load_raw_parquet(COUNTRY_ID)
    assert len(table) > 0, f"{COUNTRY_ID}: raw parquet has 0 rows"
    variables = set(table.column("variable").to_pylist())
    assert len(variables) == 10, f"expected 10 variables, got {sorted(variables)}"
    n_countries = len(set(table.column("country").to_pylist()))
    assert n_countries >= 200, f"only {n_countries} countries; listing likely truncated"
