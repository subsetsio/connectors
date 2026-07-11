-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "deposit_rate_1w",
    "deposit_rate_1m",
    "deposit_rate_3m",
    "deposit_rate_6m",
    "deposit_rate_12m",
    "savings_deposit_rate"
FROM "hkma-renminbi-deposit-rates"
