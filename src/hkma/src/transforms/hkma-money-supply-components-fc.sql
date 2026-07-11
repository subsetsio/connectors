-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "demand_deposits_with_lb",
    "m1_supply",
    "savings_deposits_with_lb",
    "time_deposits_with_lb",
    "ncds_issuedby_lb_heldby_pub",
    "m2_supply",
    "deposits_with_rlbsdtcs",
    "ncds_issuedby_rlbsdtcs_heldby_pub",
    "m3_supply"
FROM "hkma-money-supply-components-fc"
