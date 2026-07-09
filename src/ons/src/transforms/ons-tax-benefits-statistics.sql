-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "financial_and_calendar_years",
    "time",
    "uk_only",
    "geography",
    "quintile",
    "quintile_1",
    "averages_and_percentiles",
    "averagesandpercentiles",
    "income_type",
    "income",
    "value_deflation",
    "deflation"
FROM "ons-tax-benefits-statistics"
