-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Main indicators of foreign trade" AS main_indicators_of_foreign_trade,
    strptime("Month (cumulative)", '%Y-%m')::DATE AS month_cumulative,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1400-001v1-month"
