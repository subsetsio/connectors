-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "commodity_positions",
    "value"
FROM "geostat-external-20trade-exports-by-20commodities-5-export-products-2009-2019-hs-2012-6-digit-code"
