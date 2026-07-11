-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "location",
    "var",
    "obs_status",
    "obs_status_2",
    "obs_status_3",
    "aux_obs_status",
    "aux_obs_status_2",
    "conf_status",
    "time_period",
    "value"
FROM "oecd-oecd.sti.stp:dsd-sbrd@df-sbrd"
