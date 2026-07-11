-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    CAST("year" AS BIGINT) AS year,
    "groups",
    "region",
    "value"
FROM "geostat-price-20statistics-cpi-harmonised-20consumer-20price-20index-ecoicop-20rev-2-hicp-in-georgia-previous-month-100-orenovani2"
