-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple aggregation dimensions in one long table; filter aggregation before comparing or summing categories.
SELECT
    "timestep",
    "aggregation",
    "category",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "median_pay_change",
    "median_annual_pay"
FROM "adp-pay-insights"
