-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "methodology",
    "measure",
    "unit_measure",
    "expenditure",
    "adjustment",
    "transformation",
    "obs_status",
    "unit_mult",
    "base_per",
    "durability",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.tps:dsd-prices-exc-c18@df-prices-exchange-coicop18"
