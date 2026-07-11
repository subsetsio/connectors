-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "marritial_status",
    "gender",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-gender-20statistics-demography-20-mean-age-of-married-people-by-order-of-marriage"
