-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    CAST("year" AS BIGINT) AS year,
    "chapters_of_icd_10",
    "value"
FROM "geostat-demography-deaths-23-1-deaths-by-chapters-sex"
