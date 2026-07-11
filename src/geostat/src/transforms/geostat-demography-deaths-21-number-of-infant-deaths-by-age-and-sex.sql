-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "age",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-demography-deaths-21-number-of-infant-deaths-by-age-and-sex"
