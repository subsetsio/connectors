-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "order_of_marriages",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-demography-divorces-42-divorces-by-order-of-marriages-and-sex"
