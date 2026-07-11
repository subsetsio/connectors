-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "remain_1y_or_below_val",
    "remain_1y_or_below_vol",
    "remain_1yto3y_val",
    "remain_1yto3y_vol",
    "remain_3yto5y_val",
    "remain_3yto5y_vol",
    "remain_5yto7y_val",
    "remain_5yto7y_vol",
    "remain_7yto10y_val",
    "remain_7yto10y_vol",
    "remain_10yto15y_val",
    "remain_10yto15y_vol",
    "remain_total_val",
    "remain_total_vol"
FROM "hkma-govbond-turnover-remaining-tenor"
