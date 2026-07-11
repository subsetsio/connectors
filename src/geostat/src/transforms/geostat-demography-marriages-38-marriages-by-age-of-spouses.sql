-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_of_bride",
    CAST("year" AS BIGINT) AS year,
    "age_of_groom",
    "value"
FROM "geostat-demography-marriages-38-marriages-by-age-of-spouses"
