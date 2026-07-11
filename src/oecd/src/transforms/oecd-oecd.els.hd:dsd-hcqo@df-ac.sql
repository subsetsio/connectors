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
    "age",
    "sex",
    "statistical_operation",
    "income_group",
    "health_prof",
    "hspa",
    "methodology",
    "time_range",
    "survey_version",
    "decimals",
    "obs_status",
    "obs_status2",
    "obs_status3",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.els.hd:dsd-hcqo@df-ac"
