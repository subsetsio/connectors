-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "commodity_positions",
    "value"
FROM "geostat-external-20trade-exports-by-20commodities-3-export-products-1995-1999-hs-1996-4-digit-code"
