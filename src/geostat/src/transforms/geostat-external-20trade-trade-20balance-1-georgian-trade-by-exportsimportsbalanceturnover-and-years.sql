-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("years" AS BIGINT) AS years,
    "exports_imports_balance_turnover",
    "value"
FROM "geostat-external-20trade-trade-20balance-1-georgian-trade-by-exportsimportsbalanceturnover-and-years"
