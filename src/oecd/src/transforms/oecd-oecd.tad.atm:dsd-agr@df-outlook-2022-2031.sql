-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "commodity",
    "measure",
    "unit_measure",
    "version_id",
    "obs_status",
    "unit_mult",
    "decimals",
    "convention",
    "time_period",
    "value"
FROM "oecd-oecd.tad.atm:dsd-agr@df-outlook-2022-2031"
