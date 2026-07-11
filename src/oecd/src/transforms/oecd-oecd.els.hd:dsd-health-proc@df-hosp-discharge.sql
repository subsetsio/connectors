-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "medical_procedure",
    "occupation",
    "diagnostic_type",
    "provider",
    "function",
    "mode_provision",
    "care_type",
    "health_facility",
    "age",
    "sex",
    "data_srce",
    "waiting_time",
    "disease",
    "cancer_site",
    "consultation_type",
    "obs_status",
    "obs_status2",
    "obs_status3",
    "obs_status4",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.els.hd:dsd-health-proc@df-hosp-discharge"
