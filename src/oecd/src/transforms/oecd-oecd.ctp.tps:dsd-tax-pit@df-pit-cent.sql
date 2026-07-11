-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "transaction",
    "measure",
    "unit_measure",
    "sector",
    "civil_status",
    "household_type",
    "income_principal",
    "income_spouse",
    "level",
    "tax_base",
    "decimals",
    "obs_status",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.ctp.tps:dsd-tax-pit@df-pit-cent"
