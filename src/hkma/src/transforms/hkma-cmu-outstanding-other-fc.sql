-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "fixed_rate_1y_or_below",
    "fixed_rate_1yto3y",
    "fixed_rate_3yto5y",
    "fixed_rate_5yto7y",
    "fixed_rate_7y",
    "fixed_rate_subtotal",
    "floating_rate_1y_or_below",
    "floating_rate_1yto3y",
    "floating_rate_3yto5y",
    "floating_rate_5yto7y",
    "floating_rate_7y",
    "floating_rate_subtotal",
    "total"
FROM "hkma-cmu-outstanding-other-fc"
