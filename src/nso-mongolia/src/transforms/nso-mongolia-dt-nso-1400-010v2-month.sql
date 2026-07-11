-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Statistical indicator" AS statistical_indicator,
    "Main commodities" AS main_commodities,
    strptime("Month (cumulative)", '%Y-%m')::DATE AS month_cumulative,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1400-010v2-month"
