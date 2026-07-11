-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "freq",
    "obs_status",
    "unit_measure",
    "unit_mult",
    "currency",
    "base_per",
    "methodology",
    "decimals",
    "price_base",
    "adjustment",
    "time_period",
    "value"
FROM "oecd-oecd.eco.mad:dsd-eo-116@df-eo-116"
