-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "region",
    "value"
FROM "geostat-demography-deaths-20-1-number-of-deaths-by-regions-age-and-sex"
