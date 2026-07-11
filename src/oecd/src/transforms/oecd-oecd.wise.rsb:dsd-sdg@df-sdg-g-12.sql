-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "sdg_goal",
    "sdg_target",
    "sdg_indicator",
    "sdg_series",
    "age",
    "sex",
    "income_wealth_quantile",
    "education_lev",
    "deg_urb",
    "unit_measure",
    "source",
    "unit_mult",
    "price_base",
    "base_per",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.wise.rsb:dsd-sdg@df-sdg-g-12"
