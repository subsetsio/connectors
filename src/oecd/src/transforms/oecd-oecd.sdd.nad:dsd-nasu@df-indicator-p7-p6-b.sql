-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "transaction",
    "activity",
    "product",
    "unit_measure",
    "valuation",
    "price_base",
    "table_identifier",
    "counterpart_area",
    "sector",
    "accounting_entry",
    "conf_status",
    "decimals",
    "obs_status",
    "unit_mult",
    "currency",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.nad:dsd-nasu@df-indicator-p7-p6-b"
