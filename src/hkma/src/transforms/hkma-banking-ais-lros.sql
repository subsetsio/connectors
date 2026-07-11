-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "lb_incorp_hk",
    "lb_incorp_outside_hk",
    "rlb_incorp_hk",
    "rlb_incorp_outside_hk",
    "dtc_incorp_hk",
    "dtc_incorp_outside_hk",
    "all_ais",
    "lros"
FROM "hkma-banking-ais-lros"
