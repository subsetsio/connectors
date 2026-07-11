-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "instrument",
    "mechanism",
    "beneficiary",
    "stage",
    "sector",
    "unit_measure",
    "value_type",
    "energy_type",
    "energy_cat",
    "obs_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.dev.rsds:dsd-ffs@df-ffs-mkd"
