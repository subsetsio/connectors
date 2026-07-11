-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "ir_overnight",
    "ir_1w",
    "ir_1m",
    "ir_3m",
    "ir_6m",
    "ir_9m",
    "ir_12m"
FROM "hkma-interbank-rates-endperiod"
