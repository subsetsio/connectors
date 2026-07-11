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
    "plan_type",
    "definition_type",
    "vehicle_type",
    "obs_status",
    "conf_status",
    "unit_mult",
    "currency",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.daf.cm:dsd-fp@df-fps"
