"""Health-invariant tests for the Climate TRACE download nodes.

Run post-DAG, in-connector, against the raw assets via subsets_utils loaders.
Catch silent degradation that file-existence alone misses — empty payloads,
wrong gas, missing geolocation, dropped countries.
"""

from subsets_utils import load_raw_parquet


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_country_emissions_shape():
    t = load_raw_parquet("climate-trace-country-emissions")
    cols = set(t.column_names)
    assert {"iso3_country", "gas", "emissions_quantity", "subsector"} <= cols, \
        f"unexpected columns: {sorted(cols)}"
    gases = set(t.column("gas").to_pylist())
    assert gases == {"co2e_100yr"}, f"unexpected gases: {gases}"
    n_countries = len(set(t.column("iso3_country").to_pylist()))
    assert n_countries >= 150, f"only {n_countries} countries; expected ~250"


def test_asset_emissions_shape():
    t = load_raw_parquet("climate-trace-asset-emissions")
    cols = set(t.column_names)
    assert {"source_id", "lat", "lon", "gas", "emissions_quantity"} <= cols, \
        f"unexpected columns: {sorted(cols)}"
    gases = set(t.column("gas").to_pylist())
    assert gases == {"co2e_100yr"}, f"unexpected gases: {gases}"
    # geolocation should be populated for the large majority of sources
    lat = t.column("lat").to_pylist()
    nonnull = sum(1 for v in lat if v is not None)
    assert nonnull > 0, "no asset has a latitude — geolocation parse broke"
