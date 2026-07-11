-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "counterpart_area",
    "trade_flow",
    "product_type",
    "product_cpa",
    "product_hs",
    "freq",
    "unit_measure",
    "adjustment",
    "obs_status",
    "methodology_type",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.tps:dsd-bimts@df-bimts-hs2017-2d"
