-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "fc_swap_deposits",
    "deposits_hkd",
    "deposits_usd",
    "deposits_nonusd_fc",
    "deposits_all_fc",
    "deposits_all"
FROM "hkma-deposits-by-currency"
