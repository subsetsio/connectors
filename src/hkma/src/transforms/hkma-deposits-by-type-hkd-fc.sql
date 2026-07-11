-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "lb_demand_hkd",
    "lb_demand_fc",
    "lb_demand_total",
    "lb_savings_hkd",
    "lb_savings_fc",
    "lb_savings_total",
    "lb_time_hkd",
    "lb_time_fc",
    "lb_time_total",
    "lb_total_hkd",
    "lb_total_fc",
    "lb_total",
    "rlb_hkd",
    "rlb_fc",
    "rlb_total",
    "dtc_hkd",
    "dtc_fc",
    "dtc_total",
    "rlb_dtc_hkd",
    "rlb_dtc_fc",
    "rlb_dtc_total",
    "all_ais_hkd",
    "all_ais_fc",
    "all_ais_total"
FROM "hkma-deposits-by-type-hkd-fc"
