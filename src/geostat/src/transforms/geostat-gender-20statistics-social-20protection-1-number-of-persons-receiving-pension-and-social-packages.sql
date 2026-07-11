-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    CAST("year" AS BIGINT) AS year,
    "category",
    "value"
FROM "geostat-gender-20statistics-social-20protection-1-number-of-persons-receiving-pension-and-social-packages"
