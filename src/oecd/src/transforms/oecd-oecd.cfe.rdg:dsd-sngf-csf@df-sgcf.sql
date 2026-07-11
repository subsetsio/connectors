-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "sector",
    "price_base",
    "unit_measure",
    "base_per",
    "obs_status",
    "unit_mult",
    "conf_status",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.cfe.rdg:dsd-sngf-csf@df-sgcf"
