-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "measure",
    "ref_area",
    "sex",
    "deg_urb",
    "unit_measure",
    "table_id",
    "freq",
    "resourcerich",
    "unit_mult",
    "price_base",
    "base_per",
    "decimals",
    "point_info",
    "time_period",
    "value"
FROM "oecd-oecd.dev.emea:dsd-afdd-stat-annex@df-tab38"
