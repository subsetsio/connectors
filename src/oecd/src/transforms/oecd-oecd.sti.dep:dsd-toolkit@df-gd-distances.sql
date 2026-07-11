-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "policy_dim",
    "measure",
    "ref_area",
    "type",
    "latest",
    "classification",
    "direction",
    "period",
    "time_data",
    "unit_measure",
    "avg_count",
    "obs_status",
    "time_period",
    "value"
FROM "oecd-oecd.sti.dep:dsd-toolkit@df-gd-distances"
