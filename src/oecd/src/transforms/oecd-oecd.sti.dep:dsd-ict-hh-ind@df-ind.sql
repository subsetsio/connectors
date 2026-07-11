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
    "geo_area",
    "age",
    "sex",
    "education_level",
    "income_group",
    "emp_status",
    "obs_status",
    "obs_status_2",
    "obs_status_3",
    "unit_mult",
    "time_horizon_use",
    "decimals",
    "breakdown_v7_hh",
    "time_period",
    "value"
FROM "oecd-oecd.sti.dep:dsd-ict-hh-ind@df-ind"
