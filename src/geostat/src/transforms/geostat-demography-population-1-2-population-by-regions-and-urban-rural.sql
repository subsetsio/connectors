-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "urban_rural",
    CAST("year" AS BIGINT) AS year,
    "region",
    "value"
FROM "geostat-demography-population-1-2-population-by-regions-and-urban-rural"
