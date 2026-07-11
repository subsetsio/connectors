-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    CAST("years" AS BIGINT) AS years,
    "regions",
    "value"
FROM "geostat-demography-deaths-26-1-under-5-mortality-rate-by-regions-and-sex"
