-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "measure",
    "unit_measure",
    "origin",
    "training_place",
    "health_prof",
    "obs_status",
    "obs_status2",
    "obs_status3",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.els.hd:dsd-health-wfmi@df-health-wfmi"
