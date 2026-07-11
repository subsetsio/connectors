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
    "price_base",
    "transformation",
    "obs_status",
    "obs_status_2",
    "obs_status_3",
    "aux_obs_status",
    "conf_status",
    "unit_mult",
    "base_per",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.sti.stp:dsd-msti@df-msti"
