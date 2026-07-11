-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "age",
    "sex",
    "health_prof",
    "worker_status",
    "health_prof_activity_status",
    "price_base",
    "decimals",
    "obs_status",
    "obs_status2",
    "obs_status3",
    "obs_status4",
    "unit_mult",
    "ref_year_price",
    "time_period",
    "value"
FROM "oecd-oecd.els.hd:dsd-health-reac-emp@df-grad"
