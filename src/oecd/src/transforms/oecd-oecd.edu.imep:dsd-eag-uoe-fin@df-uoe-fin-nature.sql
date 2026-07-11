-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "measure",
    "ref_area",
    "education_lev",
    "exp_source",
    "exp_destination",
    "expenditure_type",
    "price_base",
    "unit_measure",
    "obs_status",
    "unit_mult",
    "decimals",
    "base_per",
    "time_period",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-uoe-fin@df-uoe-fin-nature"
