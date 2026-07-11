-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "m1_hkd",
    "m1_fc",
    "m1_total",
    "m2_hkd",
    "m2_fc",
    "m2_total",
    "m3_hkd",
    "m3_fc",
    "m3_total"
FROM "hkma-money-supply-unadjusted-fc"
