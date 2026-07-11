-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "medals",
    "age",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "sports",
    "value"
FROM "geostat-gender-20statistics-sport-20statistics-number-of-medals-won-in-non-olympic-sports"
