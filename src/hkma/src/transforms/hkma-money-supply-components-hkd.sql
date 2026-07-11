-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "legal_tender_notes_coins_in_pub",
    "demand_deposits_with_lb",
    "m1_supply",
    "savings_deposits_with_lb",
    "time_deposits_with_lb",
    "ncds_by_lb_in_pub",
    "m2_supply",
    "deposits_with_rlbsdtcs",
    "ncds_by_rlbsdtcs_in_pub",
    "m3_supply"
FROM "hkma-money-supply-components-hkd"
