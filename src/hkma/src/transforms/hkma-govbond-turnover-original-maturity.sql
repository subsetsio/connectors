-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "ad_turnover_2y",
    "ad_turnover_3y",
    "ad_turnover_5y",
    "ad_turnover_10y",
    "ad_turnover_15y",
    "ad_turnover_total"
FROM "hkma-govbond-turnover-original-maturity"
