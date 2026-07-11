-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "territorial_level",
    "ref_area",
    "territorial_type",
    "measure",
    "age",
    "sex",
    "unit_measure",
    "country",
    "obs_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.cfe.eds:dsd-reg-health@df-health"
