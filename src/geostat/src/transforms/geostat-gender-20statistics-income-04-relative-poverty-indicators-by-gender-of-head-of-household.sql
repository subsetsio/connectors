-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "median_consumption",
    "value"
FROM "geostat-gender-20statistics-income-04-relative-poverty-indicators-by-gender-of-head-of-household"
