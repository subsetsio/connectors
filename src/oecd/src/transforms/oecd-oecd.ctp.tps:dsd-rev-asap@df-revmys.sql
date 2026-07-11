-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "sector",
    "standard_revenue",
    "ctry_specific_revenue",
    "unit_measure",
    "freq",
    "obs_status",
    "unit_mult",
    "revenue_code",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.ctp.tps:dsd-rev-asap@df-revmys"
