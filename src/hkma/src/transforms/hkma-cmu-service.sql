-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "ep_no_of_cmu_members",
    "ep_no_of_dil",
    "ep_outstanding_amt_dil_with_hkd",
    "ep_outstanding_amt_dil_with_rmb",
    "ep_outstanding_amt_dil_with_usd",
    "ep_outstanding_amt_dil_with_other_curr",
    "ep_outstanding_amt_dil_with_total",
    "dp_avg_dt_hkd",
    "dp_avg_dt_rmb",
    "dp_avg_dt_usd",
    "dp_avg_dt_other_curr",
    "dp_avg_dt_total"
FROM "hkma-cmu-service"
