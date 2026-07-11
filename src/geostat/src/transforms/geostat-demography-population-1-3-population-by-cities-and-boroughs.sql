-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "urban_rural",
    CAST("year" AS BIGINT) AS year,
    "region_municipality_city_borough",
    "value"
FROM "geostat-demography-population-1-3-population-by-cities-and-boroughs"
