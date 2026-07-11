-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "order_of_marriages",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-demography-marriages-40-mean-age-of-spouses-by-order"
