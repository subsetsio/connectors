-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    CAST("year" AS BIGINT) AS year,
    "amount",
    "value"
FROM "geostat-gender-20statistics-agriculture-8-amount-of-worked-man-days-in-agricultural-holdings-by-gender"
