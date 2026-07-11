-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "commodity_positions",
    "value"
FROM "geostat-external-20trade-imports-by-20commodities-1-import-products-2020-hs-2012-4-digit-code"
