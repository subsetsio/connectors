-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "table",
    "ref_area",
    "partner_country",
    "measure",
    "activity",
    "size_class",
    "top_ent",
    "nbpartner",
    "cpc",
    "ttrader",
    "townership",
    "expint",
    "flow",
    "unit_measure",
    "obs_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.tps:dsd-tec-isic4@df-tec09"
