-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "var",
    "obs_status_1",
    "obs_status_2",
    "obs_status_3",
    "time_period",
    "value"
FROM "oecd-oecd.sti.stp:dsd-reico-cb@df-cb"
