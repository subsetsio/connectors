-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "freq",
    "ref_area",
    "measure",
    "activity",
    "methodology",
    "stri_type",
    "unit_measure",
    "counterpart_area",
    "unit_mult",
    "obs_status",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.tad.tpd:dsd-stri@df-stri-hetero"
