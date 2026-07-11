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
    "size_class",
    "age",
    "ent_type",
    "business_stage",
    "unit_measure",
    "decimals",
    "obs_status",
    "unit_mult",
    "var",
    "time_period",
    "value"
FROM "oecd-oecd.sdd.tps:dsd-sdbsbd-isic4@df-bd-emp-hg"
