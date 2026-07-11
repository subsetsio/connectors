-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "statistical_operation",
    "ownership_type",
    "health_function",
    "care_type",
    "medical_tech",
    "health_care_provider",
    "decimals",
    "obs_status",
    "obs_status2",
    "obs_status3",
    "obs_status4",
    "unit_mult",
    "ref_year_price",
    "time_period",
    "value"
FROM "oecd-oecd.els.hd:dsd-health-reac-hosp@df-beds-sect"
