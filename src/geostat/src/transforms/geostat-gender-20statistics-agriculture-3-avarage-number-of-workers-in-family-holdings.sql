-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    CAST("year" AS BIGINT) AS year,
    "region",
    "value"
FROM "geostat-gender-20statistics-agriculture-3-avarage-number-of-workers-in-family-holdings"
