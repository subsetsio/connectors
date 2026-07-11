-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "birth_order",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "region",
    "value"
FROM "geostat-demography-births-12-2-number-of-live-births-by-regions-birth-order-and-sex"
