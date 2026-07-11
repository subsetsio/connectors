-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "education_lev",
    "exp_source",
    "exp_destination",
    "expenditure_type",
    "price_base",
    "unit_measure",
    "country",
    "obs_status",
    "unit_mult",
    "decimals",
    "base_per",
    "time_period",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-subnat-uoe-fin@df-subnat-uoe-fin"
