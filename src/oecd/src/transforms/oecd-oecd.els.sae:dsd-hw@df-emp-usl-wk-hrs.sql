-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "sex",
    "age",
    "labour_force_status",
    "work_period",
    "hours_type",
    "worker_status",
    "work_time_arngmnt",
    "aggregation_operation",
    "hour_bands",
    "job_coverage",
    "obs_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.els.sae:dsd-hw@df-emp-usl-wk-hrs"
