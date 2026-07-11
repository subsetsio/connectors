-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "activity",
    "measure",
    "price_base",
    "unit_measure",
    "base_per",
    "unit_mult",
    "decimals",
    "est_method",
    "obs_status",
    "time_period",
    "value"
FROM "oecd-oecd.sti.pie:dsd-stan@df-stan-2025"
