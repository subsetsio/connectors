-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "measure",
    "category",
    "domain",
    "unit_measure",
    "activity",
    "price_base",
    "obs_status",
    "obs_status_2",
    "decimals",
    "unit_mult",
    "ref_year_price",
    "currency",
    "time_period",
    "value"
FROM "oecd-oecd.env.epi:dsd-ertr@df-ertr-acc"
