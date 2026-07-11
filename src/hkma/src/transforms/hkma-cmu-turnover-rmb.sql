-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "fixed_rate_1y_or_below_val",
    "fixed_rate_1y_or_below_vol",
    "fixed_rate_1yto3y_val",
    "fixed_rate_1yto3y_vol",
    "fixed_rate_3yto5y_val",
    "fixed_rate_3yto5y_vol",
    "fixed_rate_5yto7y_val",
    "fixed_rate_5yto7y_vol",
    "fixed_rate_7y_val",
    "fixed_rate_7y_vol",
    "fixed_rate_subtotal_val",
    "fixed_rate_subtotal_vol",
    "floating_rate_1y_or_below_val",
    "floating_rate_1y_or_below_vol",
    "floating_rate_1yto3y_val",
    "floating_rate_1yto3y_vol",
    "floating_rate_3yto5y_val",
    "floating_rate_3yto5y_vol",
    "floating_rate_5yto7y_val",
    "floating_rate_5yto7y_vol",
    "floating_rate_7y_val",
    "floating_rate_7y_vol",
    "floating_rate_subtotal_val",
    "floating_rate_subtotal_vol",
    "total_val",
    "total_vol"
FROM "hkma-cmu-turnover-rmb"
