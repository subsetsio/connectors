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
    "transport_mode",
    "vehicle_type",
    "infrastructure_type",
    "price_base",
    "obs_status",
    "obs_status2",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.itf:dsd-indicators@df-safety"
