-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "counterpart_sector",
    "transaction",
    "instr_asset",
    "pension_fundtype",
    "unit_measure",
    "price_base",
    "transformation",
    "table_identifier",
    "counterpart_area",
    "sector",
    "ref_year_price",
    "conf_status",
    "decimals",
    "obs_status",
    "unit_mult",
    "currency",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.nad:dsd-napens@df-table29"
