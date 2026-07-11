-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "measure",
    "unit_measure",
    "adjustment",
    "sector",
    "accounting_entry",
    "transaction",
    "instr_asset",
    "price_base",
    "transformation",
    "ref_year_price",
    "base_per",
    "conf_status",
    "decimals",
    "obs_status",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.nad:dsd-hhdash@df-hhdash-indic"
