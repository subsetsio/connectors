-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "unit_measure",
    "market_type",
    "pharmaceutical",
    "obs_status",
    "obs_status2",
    "obs_status3",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.els.hd:health-phmc@df-phmc-consum"
