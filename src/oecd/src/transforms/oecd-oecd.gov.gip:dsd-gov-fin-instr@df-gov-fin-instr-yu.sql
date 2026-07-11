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
    "sector",
    "instr_asset",
    "accounting_entry",
    "edition",
    "category",
    "obs_status",
    "unit_mult",
    "price_base",
    "base_per",
    "time_period",
    "value"
FROM "oecd-oecd.gov.gip:dsd-gov-fin-instr@df-gov-fin-instr-yu"
