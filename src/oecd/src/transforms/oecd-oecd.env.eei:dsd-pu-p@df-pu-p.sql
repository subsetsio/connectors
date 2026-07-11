-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "plastic_polymer",
    "plastic_app",
    "freq",
    "plastic_type",
    "scenario",
    "obs_status",
    "unit_mult",
    "unit_measure",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.env.eei:dsd-pu-p@df-pu-p"
