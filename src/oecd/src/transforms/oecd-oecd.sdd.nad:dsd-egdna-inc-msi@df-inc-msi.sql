-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "accounting_entry",
    "transaction",
    "instr_asset",
    "expenditure",
    "unit_measure",
    "income_group",
    "household_type",
    "main_income_source",
    "household_ownership",
    "age",
    "sex",
    "attainment_lev",
    "counterpart_area",
    "sector",
    "valuation",
    "price_base",
    "transformation",
    "conf_status",
    "decimals",
    "obs_status",
    "unit_mult",
    "currency",
    "labour_market_status",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.nad:dsd-egdna-inc-msi@df-inc-msi"
