-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    CAST("year" AS BIGINT) AS year,
    "indicator",
    "value"
FROM "geostat-price-20statistics-cpi-national-20consumer-20price-20index-core-inflation-to-the-same-month-of-the-previous-year"
