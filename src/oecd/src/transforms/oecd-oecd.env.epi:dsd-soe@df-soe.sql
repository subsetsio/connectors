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
    "designation",
    "ret_period",
    "decimals",
    "obs_status",
    "obs_status_2",
    "price_base",
    "ref_year_price",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.env.epi:dsd-soe@df-soe"
