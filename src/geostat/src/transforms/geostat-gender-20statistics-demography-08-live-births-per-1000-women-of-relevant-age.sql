-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-gender-20statistics-demography-08-live-births-per-1000-women-of-relevant-age"
